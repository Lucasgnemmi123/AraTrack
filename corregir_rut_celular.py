"""
Script para corregir el intercambio de valores entre RUT y CELULAR en la tabla choferes
"""
import sqlite3

def corregir_choferes():
    """Intercambiar valores de rut y celular en la tabla choferes"""
    
    conn = sqlite3.connect('viajes.db')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("CORRECCIÓN DE COLUMNAS RUT Y CELULAR EN CHOFERES")
    print("="*60)
    
    # Mostrar algunos registros antes
    print("\n📋 ANTES DE LA CORRECCIÓN (primeros 5 registros):")
    cursor.execute('SELECT nombre, rut, celular FROM maestras_choferes LIMIT 5')
    registros_antes = cursor.fetchall()
    for nombre, rut, celular in registros_antes:
        print(f"  {nombre[:30]:30} | RUT: {rut:15} | CEL: {celular}")
    
    # Contar registros
    cursor.execute('SELECT COUNT(*) FROM maestras_choferes')
    total = cursor.fetchone()[0]
    print(f"\n📊 Total de choferes a corregir: {total}")
    
    # Realizar el intercambio usando una columna temporal
    print("\n🔄 Intercambiando valores...")
    
    # Crear tabla nueva sin constraint UNIQUE en rut
    cursor.execute('''
        CREATE TABLE maestras_choferes_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            rut TEXT,
            celular TEXT
        )
    ''')
    
    # Copiar datos con los valores intercambiados (celular → rut, rut → celular)
    cursor.execute('''
        INSERT INTO maestras_choferes_new (id, nombre, rut, celular)
        SELECT id, nombre, celular, rut FROM maestras_choferes
    ''')
    
    # Eliminar tabla vieja
    cursor.execute('DROP TABLE maestras_choferes')
    
    # Renombrar tabla nueva
    cursor.execute('ALTER TABLE maestras_choferes_new RENAME TO maestras_choferes')
    
    conn.commit()
    
    # Mostrar registros después
    print("\n✅ DESPUÉS DE LA CORRECCIÓN (primeros 5 registros):")
    cursor.execute('SELECT nombre, rut, celular FROM maestras_choferes LIMIT 5')
    registros_despues = cursor.fetchall()
    for nombre, rut, celular in registros_despues:
        print(f"  {nombre[:30]:30} | RUT: {rut:15} | CEL: {celular}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ CORRECCIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print(f"\n📌 {total} choferes actualizados")
    print("📌 Columnas RUT y CELULAR intercambiadas correctamente\n")

if __name__ == '__main__':
    try:
        corregir_choferes()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
