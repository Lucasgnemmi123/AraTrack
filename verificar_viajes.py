import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('viajes.db')
cursor = conn.cursor()

# Verificar viajes
cursor.execute("SELECT COUNT(*) FROM viajes")
total = cursor.fetchone()[0]
print(f"\n✓ Total de viajes en la base de datos: {total}")

if total > 0:
    cursor.execute("SELECT DISTINCT numero_viaje FROM viajes ORDER BY numero_viaje LIMIT 10")
    viajes = cursor.fetchall()
    print("\n📋 Primeros 10 números de viaje:")
    for viaje in viajes:
        print(f"   - {viaje[0]}")
    
    # Mostrar ejemplo con centros
    cursor.execute("""
        SELECT numero_viaje, costo_codigo, COUNT(*) as cantidad
        FROM viajes 
        GROUP BY numero_viaje, costo_codigo
        ORDER BY numero_viaje DESC
        LIMIT 5
    """)
    print("\n📊 Últimos 5 viajes con sus centros de costo:")
    for row in cursor.fetchall():
        print(f"   Viaje {row[0]} → Centro {row[1]} ({row[2]} registro(s))")
else:
    print("\n⚠️ NO HAY VIAJES en la base de datos")
    print("   Necesitas crear al menos un viaje para poder editarlo.")

conn.close()
