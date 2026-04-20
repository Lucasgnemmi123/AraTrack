"""
Crear plantilla Excel para ingresar datos de viajes del 02-05 de abril
Con validación de maestras de casinos y choferes
"""
import pandas as pd
import sqlite3
from datetime import datetime

print("=== CREANDO PLANTILLA EXCEL PARA DATOS FALTANTES ===\n")

# Conectar a la BD para obtener el último ID y las maestras
conn = sqlite3.connect('viajes.db')
cur = conn.cursor()

# Obtener último ID
cur.execute("SELECT MAX(id) FROM viajes")
ultimo_id = cur.fetchone()[0]
print(f"Último ID en base de datos: {ultimo_id}")

# Obtener maestras de casinos
cur.execute("SELECT nombre FROM maestras_casinos ORDER BY nombre")
casinos = [row[0] for row in cur.fetchall()]
print(f"Casinos en maestra: {len(casinos)}")

# Obtener maestras de choferes  
cur.execute("SELECT nombre, rut FROM maestras_choferes ORDER BY nombre")
choferes = cur.fetchall()
print(f"Choferes en maestra: {len(choferes)}")

conn.close()

# Crear estructura para viajes (columnas principales)
columnas_viajes = [
    'numero_viaje', 'casino', 'ruta', 'tipo_camion', 'patente_camion', 
    'patente_semi', 'numero_rampa', 'transporte', 'costo_codigo',
    'termografos_gps', 'fecha', 'fecha_hora_llegada_dhl', 'fecha_hora_salida_dhl',
    'conductor', 'celular', 'rut', 'numero_camion', 'num_wencos', 'bin',
    'pallets', 'pallets_chep', 'pallets_pl_negro_grueso', 'pallets_pl_negro_alternativo',
    'pallets_refrigerado', 'wencos_refrigerado', 'pallets_congelado', 'wencos_congelado',
    'pallets_abarrote', 'check_congelado', 'check_refrigerado', 'check_abarrote',
    'check_implementos', 'check_aseo', 'check_trazabilidad', 'check_plataforma_wtck',
    'check_env_correo_wtck', 'check_revision_planilla_despacho',
    'guia_1', 'guia_2', 'guia_3', 'guia_4', 'guia_5', 'guia_6', 'guia_7', 'guia_8',
    'guia_9', 'guia_10', 'guia_11', 'guia_12', 'guia_13', 'guia_14', 'guia_15',
    'guia_16', 'guia_17', 'guia_18', 'guia_19', 'guia_20', 'guia_21',
    'sello_salida_1p', 'sello_salida_2p', 'sello_salida_3p', 'sello_salida_4p',
    'sello_salida_5p', 'sello_retorno_1p', 'sello_retorno_2p', 'sello_retorno_3p',
    'sello_retorno_4p', 'sello_retorno_5p', 'numero_certificado_fumigacion',
    'revision_limpieza_camion_acciones', 'administrativo_responsable'
]

# Crear DataFrame vacío para viajes
df_viajes = pd.DataFrame(columns=columnas_viajes)

# Agregar filas de ejemplo para facilitar el llenado
ejemplos = []
for dia in ['02', '03', '04', '05']:
    ejemplos.append({
        'numero_viaje': f'Ejemplo_{dia}',
        'fecha': f'2026-04-{dia}',
        'casino': 'Seleccionar de la hoja Maestras',
        'conductor': 'Nombre completo del conductor',
        'rut': '12.345.678-9',
        'patente_camion': 'ABCD-12',
        'transporte': 'Nombre empresa transporte',
        'tipo_camion': '12 Toneladas',
        'ruta': 'Ciudad',
        'costo_codigo': '12345',
    })

df_viajes_ejemplo = pd.DataFrame(ejemplos)

# Crear estructura para comidas preparadas
columnas_comidas = [
    'numero_viaje', 'numero_centro_costo', 'guia_comida', 'descripcion',
    'kilo', 'bultos', 'proveedor'
]

df_comidas = pd.DataFrame(columns=columnas_comidas)

# Ejemplos de comidas
ejemplos_comidas = [
    {
        'numero_viaje': 'Ejemplo_02',
        'numero_centro_costo': '30922',
        'guia_comida': '123456',
        'descripcion': 'IMPL',
        'kilo': 0.0,
        'bultos': 1,
        'proveedor': 'YARUR'
    }
]

df_comidas_ejemplo = pd.DataFrame(ejemplos_comidas)

# Crear hojas de maestras para referencia
df_maestras_casinos = pd.DataFrame({'casino': casinos})
df_maestras_choferes = pd.DataFrame({
    'nombre': [c[0] for c in choferes],
    'rut': [c[1] for c in choferes]
})

# Generar archivo Excel
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"plantilla_viajes_02_05_abril_{timestamp}.xlsx"

print(f"\nGenerando archivo: {output_file}")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Hoja 1: Instrucciones
    instrucciones = pd.DataFrame({
        'INSTRUCCIONES': [
            '1. Esta plantilla es para ingresar los viajes del 02-05 de abril que faltan',
            f'2. El último ID en la base de datos es: {ultimo_id}',
            '3. Los nuevos registros se insertarán a partir del ID siguiente',
            '4. NO reemplazarán datos existentes - solo se agregarán',
            '5. Revisa las hojas "Maestras_Casinos" y "Maestras_Choferes" para validar nombres',
            '6. Si un casino o chofer no existe, anótalo en la hoja "Nuevas_Maestras"',
            '7. Completa la hoja "VIAJES" con los datos de cada viaje',
            '8. Completa la hoja "COMIDAS_PREPARADAS" si hay comidas preparadas',
            '9. Borra las filas de ejemplo antes de importar',
            '10. Guarda el archivo cuando termines y avísame para importar los datos',
            '',
            'IMPORTANTE:',
            '- La fecha debe estar en formato: YYYY-MM-DD (ejemplo: 2026-04-02)',
            '- El RUT debe incluir guión (ejemplo: 12.345.678-9)',
            '- Los checks deben ser "X" o dejar vacío'
        ]
    })
    instrucciones.to_excel(writer, sheet_name='INSTRUCCIONES', index=False)
    
    # Hoja 2: Viajes - con ejemplos
    df_viajes_ejemplo.to_excel(writer, sheet_name='VIAJES', index=False)
    
    # Hoja 3: Comidas preparadas - con ejemplos
    df_comidas_ejemplo.to_excel(writer, sheet_name='COMIDAS_PREPARADAS', index=False)
    
    # Hoja 4: Maestras Casinos (referencia)
    df_maestras_casinos.to_excel(writer, sheet_name='Maestras_Casinos', index=False)
    
    # Hoja 5: Maestras Choferes (referencia)
    df_maestras_choferes.to_excel(writer, sheet_name='Maestras_Choferes', index=False)
    
    # Hoja 6: Nuevas maestras a crear
    df_nuevas = pd.DataFrame({
        'tipo': ['casino', 'chofer'],
        'nombre': ['', ''],
        'rut': ['', '(solo para choferes)']
    })
    df_nuevas.to_excel(writer, sheet_name='Nuevas_Maestras', index=False)

print(f"✓ Plantilla generada: {output_file}\n")
print("PRÓXIMOS PASOS:")
print("=" * 80)
print("1. Abre el archivo Excel generado")
print("2. Revisa los PDFs del 02-05 de abril (carpeta pdfs/)")
print("3. Completa los datos en la hoja VIAJES")
print("4. Si hay comidas preparadas, complétalas en COMIDAS_PREPARADAS")
print("5. Verifica que casinos/choferes existan en las maestras")
print("6. Si falta alguno, anótalo en la hoja Nuevas_Maestras")
print("7. Borra las filas de ejemplo")
print("8. Guarda el archivo y avísame para importar los datos")
print("=" * 80)
