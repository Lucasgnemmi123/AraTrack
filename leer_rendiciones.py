import pandas as pd

# Intentar múltiples métodos para leer el archivo
print("=" * 60)
print("ANALIZANDO ARCHIVO RENDICIONES")
print("=" * 60)

# Método 1: Intentar con openpyxl (si existe versión xlsx)
try:
    print("\n🔍 Intentando leer como .xlsx...")
    df = pd.read_excel('Rendiciones.xlsx', engine='openpyxl')
    print("✓ Archivo leído exitosamente con openpyxl")
except Exception as e:
    print(f"✗ No se pudo leer como .xlsx: {e}")
    
    # Método 2: Intentar leer xlsb sin engine específico
    try:
        print("\n🔍 Intentando leer .xlsb sin engine...")
        df = pd.read_excel('Rendiciones.xlsb')
        print("✓ Archivo leído exitosamente")
    except Exception as e2:
        print(f"✗ Error: {e2}")
        print("\n⚠️ NO SE PUDO LEER EL ARCHIVO")
        print("\nPor favor, convierte 'Rendiciones.xlsb' a 'Rendiciones.xlsx'")
        print("Abre el archivo en Excel y guárdalo como .xlsx")
        exit(1)

print(f"\n📊 Total de registros: {len(df)}")
print(f"\n📋 Columnas ({len(df.columns)}):")
print("-" * 60)

for i, col in enumerate(df.columns, 1):
    # Obtener un valor de ejemplo (no nulo si es posible)
    ejemplo = None
    for val in df[col]:
        if pd.notna(val) and str(val).strip() != '':
            ejemplo = val
            break
    
    tipo = df[col].dtype
    print(f"{i:2d}. {col:40s} | Tipo: {str(tipo):15s} | Ej: {ejemplo}")

print("\n" + "=" * 60)
print("PRIMERAS 5 FILAS:")
print("=" * 60)
print(df.head(5).to_string())

print("\n" + "=" * 60)
print("SQL CREATE TABLE SUGERIDO:")
print("=" * 60)
print("CREATE TABLE rendiciones (")
for i, col in enumerate(df.columns):
    col_name = col.lower().replace(' ', '_').replace('°', '').replace('/', '_')
    col_type = "TEXT"
    if 'fecha' in col.lower():
        col_type = "DATE"
    elif df[col].dtype in ['int64', 'float64']:
        col_type = "REAL"
    
    coma = "," if i < len(df.columns) - 1 else ""
    print(f"    {col_name} {col_type}{coma}")

print("    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,")
print("    fecha_modificacion DATETIME,")
print("    rendicion TEXT DEFAULT 'SIN REVISAR'")
print(");")

