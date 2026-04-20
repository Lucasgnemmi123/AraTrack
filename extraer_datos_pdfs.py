"""
Extractor de datos desde PDFs de viajes
Extrae información para tablas viajes y comidas_preparadas
"""
import os
import re
from datetime import datetime
import pandas as pd
try:
    import PyPDF2
except ImportError:
    print("Instalando PyPDF2...")
    os.system("pip install PyPDF2")
    import PyPDF2

print("=== EXTRACTOR DE DATOS DE PDFs ===\n")

# Obtener lista de PDFs del 01-05 de abril
pdfs_folder = "pdfs"
pdf_files = []

for filename in os.listdir(pdfs_folder):
    if filename.endswith("_completo.pdf"):
        filepath = os.path.join(pdfs_folder, filename)
        mod_time = os.path.getmtime(filepath)
        mod_date = datetime.fromtimestamp(mod_time)
        
        # Filtrar PDFs modificados entre 01-05 de abril
        if mod_date >= datetime(2026, 4, 1) and mod_date < datetime(2026, 4, 6):
            pdf_files.append({
                'filename': filename,
                'filepath': filepath,
                'mod_date': mod_date,
                'numero_viaje': filename.replace('viaje_', '').replace('_completo.pdf', '')
            })

pdf_files.sort(key=lambda x: x['mod_date'])

print(f"PDFs encontrados: {len(pdf_files)}")
print(f"Rango de fechas: {pdf_files[0]['mod_date'].strftime('%Y-%m-%d')} a {pdf_files[-1]['mod_date'].strftime('%Y-%m-%d')}\n")

# Función para extraer texto de un PDF
def extraer_texto_pdf(filepath):
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto = ""
            for page in pdf_reader.pages:
                texto += page.extract_text() + "\n"
            return texto
    except Exception as e:
        print(f"  Error al leer {filepath}: {e}")
        return ""

# Función para extraer datos de viaje del texto
def extraer_datos_viaje(texto, numero_viaje):
    datos = {
        'numero_viaje': numero_viaje,
        'casino': '',
        'ruta': '',
        'tipo_camion': '',
        'patente_camion': '',
        'patente_semi': '',
        'numero_rampa': '',
        'transporte': '',
        'costo_codigo': '',
        'termografos_gps': '',
        'fecha': '',
        'fecha_hora_llegada_dhl': '',
        'fecha_hora_salida_dhl': '',
        'conductor': '',
        'celular': '',
        'rut': '',
        'numero_camion': '',
        'num_wencos': '',
        'bin': '',
        'pallets': '',
        'pallets_chep': '',
        'pallets_pl_negro_grueso': '',
        'pallets_pl_negro_alternativo': '',
        'pallets_refrigerado': '',
        'wencos_refrigerado': '',
        'pallets_congelado': '',
        'wencos_congelado': '',
        'pallets_abarrote': '',
    }
    
    # Extraer campos usando patrones
    # Número viaje ya lo tenemos
    
    # Casino/Cliente
    match = re.search(r'CLIENTE[:\s]+(.+?)(?:\n|RUTA)', texto, re.IGNORECASE)
    if match:
        datos['casino'] = match.group(1).strip()
    
    # Ruta
    match = re.search(r'RUTA[:\s]+(.+?)(?:\n|TIPO)', texto, re.IGNORECASE)
    if match:
        datos['ruta'] = match.group(1).strip()
    
    # Fecha
    match = re.search(r'FECHA[:\s]+(\d{4}-\d{2}-\d{2})', texto)
    if match:
        datos['fecha'] = match.group(1)
    
    # Patente camión
    match = re.search(r'PATENTE CAMION[:\s]+([A-Z]{2,4}[-\s]?\d{2,3})', texto, re.IGNORECASE)
    if match:
        datos['patente_camion'] = match.group(1).strip()
    
    # Patente semi
    match = re.search(r'PATENTE SEMI[:\s]+([A-Z]{2,4}[-\s]?\d{2,4})', texto, re.IGNORECASE)
    if match:
        datos['patente_semi'] = match.group(1).strip()
    
    # Transporte
    match = re.search(r'TRANSPORTE[:\s]+(.+?)(?:\n|TIPO)', texto, re.IGNORECASE)
    if match:
        datos['transporte'] = match.group(1).strip()
    
    # Tipo camión
    match = re.search(r'TIPO CAMION[:\s]+(.+?)(?:\n|TERMOGRAFOS)', texto, re.IGNORECASE)
    if match:
        datos['tipo_camion'] = match.group(1).strip()
    
    # Conductor
    match = re.search(r'CONDUCTOR[:\s]+(.+?)(?:\n|N°|RUT)', texto, re.IGNORECASE)
    if match:
        datos['conductor'] = match.group(1).strip()
    
    # RUT
    match = re.search(r'RUT[:\s]+(\d{1,2}[.\s]?\d{3}[.\s]?\d{3}[-\s]?[\dkK])', texto, re.IGNORECASE)
    if match:
        datos['rut'] = match.group(1).strip()
    
    # Centro de costo
    match = re.search(r'CODIGO[:\s]+(\d+)', texto, re.IGNORECASE)
    if match:
        datos['costo_codigo'] = match.group(1)
    
    # Número de rampa
    match = re.search(r'N°\s*DE\s*RAMPLA[:\s]+([A-Z0-9-]+)', texto, re.IGNORECASE)
    if match:
        datos['numero_rampa'] = match.group(1).strip()
    
    # Número de camión
    match = re.search(r'N°\s*CAMION[:\s]+([A-Z0-9-]+)', texto, re.IGNORECASE)
    if match:
        datos['numero_camion'] = match.group(1).strip()
    
    # Wencos
    match = re.search(r'WENCOS[:\s]+(\d+)', texto, re.IGNORECASE)
    if match:
        datos['num_wencos'] = match.group(1)
    
    # Pallets
    match = re.search(r'PALLETS[:\s]+(\d+)', texto, re.IGNORECASE)
    if match:
        datos['pallets'] = match.group(1)
    
    return datos

# Función para extraer comidas preparadas del texto
def extraer_comidas_preparadas(texto, numero_viaje):
    comidas = []
    
    # Buscar sección de comidas preparadas o guías
    # Patrón para guías: número de guía, descripción, kilos, bultos
    patron_guia = r'(\d{5,8})\s+([A-Z\s]+?)\s+(\d+[\.,]?\d*)\s+(\d+)'
    
    matches = re.finditer(patron_guia, texto)
    for match in matches:
        guia = match.group(1)
        descripcion = match.group(2).strip()
        kilos = match.group(3).replace(',', '.')
        bultos = match.group(4)
        
        # Filtrar solo si parece ser comida preparada (IMPL, REF, CONG, etc)
        if any(word in descripcion.upper() for word in ['IMPL', 'REF', 'CONG', 'ABARR']):
            comidas.append({
                'numero_viaje': numero_viaje,
                'guia_comida': guia,
                'descripcion': descripcion,
                'kilo': float(kilos) if kilos else 0.0,
                'bultos': int(bultos) if bultos else 0,
                'proveedor': '',
                'numero_centro_costo': ''
            })
    
    return comidas

# Procesar PDFs
print("Procesando PDFs...\n")
viajes_data = []
comidas_data = []
errores = []

for i, pdf_info in enumerate(pdf_files, 1):
    print(f"{i}/{len(pdf_files)} - {pdf_info['filename']}")
    
    texto = extraer_texto_pdf(pdf_info['filepath'])
    
    if not texto:
        errores.append(pdf_info['filename'])
        continue
    
    # Extraer datos de viaje
    datos_viaje = extraer_datos_viaje(texto, pdf_info['numero_viaje'])
    viajes_data.append(datos_viaje)
    
    # Extraer comidas preparadas
    comidas = extraer_comidas_preparadas(texto, pdf_info['numero_viaje'])
    comidas_data.extend(comidas)

print(f"\n✓ Viajes extraídos: {len(viajes_data)}")
print(f"✓ Comidas preparadas extraídas: {len(comidas_data)}")
if errores:
    print(f"✗ PDFs con errores: {len(errores)}")

# Crear Excel con dos hojas
print("\nGenerando Excel...")
output_file = f"datos_extraidos_pdfs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Hoja de viajes
    df_viajes = pd.DataFrame(viajes_data)
    df_viajes.to_excel(writer, sheet_name='viajes', index=False)
    
    # Hoja de comidas preparadas
    if comidas_data:
        df_comidas = pd.DataFrame(comidas_data)
        df_comidas.to_excel(writer, sheet_name='comidas_preparadas', index=False)
    else:
        # Crear hoja vacía con estructura
        df_comidas = pd.DataFrame(columns=['numero_viaje', 'guia_comida', 'descripcion', 'kilo', 'bultos', 'proveedor', 'numero_centro_costo'])
        df_comidas.to_excel(writer, sheet_name='comidas_preparadas', index=False)

print(f"✓ Excel generado: {output_file}")

# Mostrar resumen por fecha
print("\nResumen por fecha:")
df_viajes_temp = pd.DataFrame(viajes_data)
if not df_viajes_temp.empty and 'fecha' in df_viajes_temp.columns:
    fecha_counts = df_viajes_temp['fecha'].value_counts().sort_index()
    for fecha, count in fecha_counts.items():
        if fecha:
            print(f"  {fecha}: {count} viajes")
else:
    print("  No se pudieron extraer fechas")

print(f"\n✓ Archivo listo para revisión: {output_file}")
print("\nNOTA: Revisa el Excel y completa los campos faltantes antes de importar.")
