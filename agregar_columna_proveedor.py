"""
Script para agregar la columna 'proveedor' a la tabla comidas_preparadas
sin perder los datos existentes.
"""
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('viajes.db')
cursor = conn.cursor()

try:
    # Verificar si la columna ya existe
    cursor.execute("PRAGMA table_info(comidas_preparadas)")
    columnas = [col[1] for col in cursor.fetchall()]
    
    if 'proveedor' not in columnas:
        print("Agregando columna 'proveedor' a la tabla comidas_preparadas...")
        cursor.execute('ALTER TABLE comidas_preparadas ADD COLUMN proveedor TEXT')
        conn.commit()
        print("✅ Columna 'proveedor' agregada exitosamente")
    else:
        print("ℹ️  La columna 'proveedor' ya existe en la tabla")
    
    # Mostrar estructura actualizada
    cursor.execute("PRAGMA table_info(comidas_preparadas)")
    print("\n📋 Estructura actual de la tabla comidas_preparadas:")
    for col in cursor.fetchall():
        print(f"   - {col[1]} ({col[2]})")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
    print("\n✅ Proceso completado")
