import sqlite3

# Conectar a la base de datos del portable
conn = sqlite3.connect(r'AraTrack_Portable\viajes.db')
cursor = conn.cursor()

# Listar tablas
print("=== TABLAS EN viajes.db (Portable) ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f"- {table[0]}")

# Verificar si existe tabla rendiciones
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rendiciones'")
rendiciones = cursor.fetchone()

if rendiciones:
    print("\n✅ Tabla 'rendiciones' existe")
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM rendiciones")
    count = cursor.fetchone()[0]
    print(f"   Total de rendiciones: {count}")
    
    # Mostrar estructura
    cursor.execute("PRAGMA table_info(rendiciones)")
    columns = cursor.fetchall()
    print("\n   Columnas:")
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
else:
    print("\n❌ Tabla 'rendiciones' NO existe")

conn.close()
