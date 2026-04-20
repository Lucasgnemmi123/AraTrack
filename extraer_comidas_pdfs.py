"""
Extraer comidas preparadas desde PDFs
Cada página del PDF corresponde a un centro de costo diferente
"""
import os
import re
import sqlite3
from datetime import datetime
import PyPDF2

print("=== EXTRACCIÓN DE COMIDAS PREPARADAS DESDE PDFs ===\n")

# Conectar a BD
conn = sqlite3.connect('viajes.db')
cur = conn.cursor()

# Obtener viajes del 02-04 sin comidas preparadas
print("Identificando viajes del 02-04 de abril sin comidas...")
cur.execute("""
    SELECT DISTINCT v.numero_viaje, v.fecha
    FROM viajes v
    LEFT JOIN comidas_preparadas cp ON v.numero_viaje = cp.numero_viaje
    WHERE v.fecha IN ('2026-04-02', '2026-04-03', '2026-04-04')
    GROUP BY v.numero_viaje, v.fecha
    HAVING COUNT(cp.id) = 0
    ORDER BY v.fecha, v.numero_viaje
""")
viajes_sin_comidas = {row[0]: row[1] for row in cur.fetchall()}
print(f"✓ Viajes sin comidas preparadas: {len(viajes_sin_comidas)}\n")

# Obtener lista de PDFs del 02-04 de abril
pdfs_folder = "pdfs"
pdfs_procesar = []

for filename in os.listdir(pdfs_folder):
    if filename.endswith("_completo.pdf"):
        # Extraer número de viaje del nombre
        numero_viaje = filename.replace('viaje_', '').replace('_completo.pdf', '')
        
        # Verificar si este viaje necesita comidas preparadas
        if numero_viaje in viajes_sin_comidas:
            filepath = os.path.join(pdfs_folder, filename)
            pdfs_procesar.append({
                'filename': filename,
                'filepath': filepath,
                'numero_viaje': numero_viaje,
                'fecha': viajes_sin_comidas[numero_viaje]
            })

pdfs_procesar.sort(key=lambda x: (x['fecha'], x['numero_viaje']))
print(f"PDFs a procesar: {len(pdfs_procesar)}")

if len(pdfs_procesar) == 0:
    print("✓ No hay PDFs para procesar")
    conn.close()
    exit(0)

print(f"Primeros 10 PDFs: {[p['filename'] for p in pdfs_procesar[:10]]}\n")

# Función para extraer centro de costo de la página
def extraer_centro_costo(texto_pagina):
    """Buscar número de centro de costo en el texto"""
    # Patrones: "CENTRO DE COSTO: 12345", "CC: 12345", "CODIGO: 12345"
    patrones = [
        r'CENTRO\s+DE\s+COSTO[:\s]+(\d{4,6})',
        r'C\.?C\.?[:\s]+(\d{4,6})',
        r'CODIGO[:\s]+COSTO[:\s]+(\d{4,6})',
        r'COSTO[:\s]+CODIGO[:\s]+(\d{4,6})'
    ]
    
    for patron in patrones:
        match = re.search(patron, texto_pagina, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

# Función para extraer tabla de comidas de la página
def extraer_comidas_pagina(texto_pagina, numero_viaje, centro_costo):
    """Extraer comidas preparadas de una página"""
    comidas = []
    
    # Buscar tabla con formato: GUÍA | DESCRIPCIÓN | KILOS | BULTOS | PROVEEDOR
    # Pueden estar en secciones como "IMPLEMENTOS", "COMIDAS PREPARADAS", etc.
    
    # Patrón para líneas de tabla: número_guía descripción kilos bultos proveedor
    # Ejemplo: "1234567  IMPL  0.0  1  YARUR"
    patron_linea = r'(\d{5,8})\s+([A-Z\s]{2,20}?)\s+(\d+[\.,]?\d*)\s+(\d+)\s*([A-Z\s]*?)(?:\n|$)'
    
    matches = re.finditer(patron_linea, texto_pagina)
    for match in matches:
        guia = match.group(1).strip()
        desc = match.group(2).strip()
        kilos_str = match.group(3).replace(',', '.')
        bultos_str = match.group(4)
        proveedor = match.group(5).strip() if match.group(5) else ''
        
        # Validar que sea una línea de datos válida
        if len(guia) >= 5 and len(desc) >= 2:
            try:
                kilos = float(kilos_str)
                bultos = int(bultos_str)
                
                comidas.append({
                    'numero_viaje': numero_viaje,
                    'numero_centro_costo': centro_costo or '',
                    'guia_comida': guia,
                    'descripcion': desc,
                    'kilo': kilos,
                    'bultos': bultos,
                    'proveedor': proveedor or ''
                })
            except:
                pass
    
    return comidas

# Procesar PDFs
print("Procesando PDFs...\n")
print("-" * 80)

total_comidas_extraidas = 0
pdfs_procesados = 0
pdfs_con_error = 0

# Crear backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_path = f"_backups_bd/viajes_antes_comidas_pdf_{timestamp}.db"
print(f"Creando backup: {backup_path}\n")
import shutil
shutil.copy2('viajes.db', backup_path)

for i, pdf_info in enumerate(pdfs_procesar, 1):
    try:
        # Leer PDF
        with open(pdf_info['filepath'], 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_paginas = len(pdf_reader.pages)
            
            comidas_viaje = []
            
            # Procesar cada página (cada centro de costo)
            for page_num in range(num_paginas):
                page = pdf_reader.pages[page_num]
                texto_pagina = page.extract_text()
                
                # Extraer centro de costo de esta página
                centro_costo = extraer_centro_costo(texto_pagina)
                
                # Extraer comidas de esta página
                comidas_pagina = extraer_comidas_pagina(texto_pagina, pdf_info['numero_viaje'], centro_costo)
                comidas_viaje.extend(comidas_pagina)
            
            # Insertar comidas en BD
            if comidas_viaje:
                insert_query = """
                    INSERT INTO comidas_preparadas 
                    (numero_viaje, numero_centro_costo, guia_comida, descripcion, kilo, bultos, proveedor)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                
                for comida in comidas_viaje:
                    try:
                        cur.execute(insert_query, (
                            comida['numero_viaje'],
                            comida['numero_centro_costo'],
                            comida['guia_comida'],
                            comida['descripcion'],
                            comida['kilo'],
                            comida['bultos'],
                            comida['proveedor']
                        ))
                        total_comidas_extraidas += 1
                    except Exception as e:
                        pass
                
                conn.commit()
                print(f"✓ {i:3d}/{len(pdfs_procesar)} | Viaje {pdf_info['numero_viaje']:8s} | {num_paginas} pág | {len(comidas_viaje)} comidas")
                pdfs_procesados += 1
            else:
                print(f"⚠ {i:3d}/{len(pdfs_procesar)} | Viaje {pdf_info['numero_viaje']:8s} | Sin comidas detectadas")
                
    except Exception as e:
        print(f"✗ {i:3d}/{len(pdfs_procesar)} | Viaje {pdf_info['numero_viaje']:8s} | Error: {str(e)[:50]}")
        pdfs_con_error += 1
    
    # Mostrar progreso cada 20 PDFs
    if i % 20 == 0:
        print(f"   Progreso: {i}/{len(pdfs_procesar)} - {total_comidas_extraidas} comidas extraídas")

print("\n" + "="*80)
print("RESUMEN:")
print("="*80)
print(f"✓ PDFs procesados exitosamente: {pdfs_procesados}")
print(f"✓ Comidas preparadas extraídas: {total_comidas_extraidas}")
print(f"✗ PDFs con error: {pdfs_con_error}")

# Estado final
print("\n" + "="*80)
print("ESTADO FINAL:")
print("="*80)
cur.execute("""
    SELECT v.fecha, COUNT(cp.id) as total_comidas
    FROM viajes v
    LEFT JOIN comidas_preparadas cp ON v.numero_viaje = cp.numero_viaje
    WHERE v.fecha LIKE '2026-04-%'
    GROUP BY v.fecha
    ORDER BY v.fecha
""")
for fecha, count in cur.fetchall():
    print(f"  {fecha}: {count} comidas preparadas")

conn.close()
print(f"\n✓ Proceso completado")
print(f"✓ Backup guardado: {backup_path}")
