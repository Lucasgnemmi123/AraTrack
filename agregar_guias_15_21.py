"""
Script para agregar columnas guia_15 hasta guia_21 a la base de datos
Ejecutar una sola vez para actualizar la estructura
"""
import sqlite3

def agregar_columnas_guias():
    conn = sqlite3.connect('viajes.db')
    cursor = conn.cursor()
    
    # Verificar si ya existen las columnas
    cursor.execute("PRAGMA table_info(viajes)")
    columnas_existentes = [col[1] for col in cursor.fetchall()]
    
    print("Agregando columnas guia_15 hasta guia_21...")
    
    # Agregar columnas guia_15 a guia_21
    for i in range(15, 22):
        columna = f'guia_{i}'
        if columna not in columnas_existentes:
            try:
                cursor.execute(f"ALTER TABLE viajes ADD COLUMN {columna} TEXT DEFAULT ''")
                print(f"✓ Columna {columna} agregada exitosamente")
            except sqlite3.OperationalError as e:
                print(f"✗ Error al agregar {columna}: {e}")
        else:
            print(f"⚠ Columna {columna} ya existe, omitiendo")
    
    conn.commit()
    conn.close()
    print("\n✓ Base de datos actualizada correctamente")
    print("Ahora tienes 21 campos para guías (guia_1 hasta guia_21)")

if __name__ == '__main__':
    agregar_columnas_guias()
