"""
Verificar qué fechas debes usar para incluir los 36 viajes del 1 de abril
"""
import sqlite3
from datetime import datetime

DB_DESTINO = r"C:\DHL_Viajes\viajes.db"

conn = sqlite3.connect(DB_DESTINO)
cursor = conn.cursor()

print("="*80)
print("GUÍA PARA GENERAR REPORTE CON LOS 36 VIAJES DEL 1 DE ABRIL")
print("="*80)

# Ver la distribución de viajes por fecha en abril
cursor.execute("""
    SELECT fecha, COUNT(*) as total
    FROM viajes
    WHERE fecha LIKE '2026-04%'
    GROUP BY fecha
    ORDER BY fecha
""")

viajes_abril = cursor.fetchall()

print("\n📅 VIAJES POR FECHA EN ABRIL 2026:")
print("-"*80)
for fecha, total in viajes_abril:
    print(f"   {fecha}: {total} viajes")

# Específicamente el 1 de abril
cursor.execute("""
    SELECT COUNT(*) as total
    FROM viajes
    WHERE fecha = '2026-04-01'
""")
total_1_abril = cursor.fetchone()[0]

print("\n" + "="*80)
print("CONFIGURACIÓN DEL REPORTE")
print("="*80)
print(f"\n✅ Para obtener los {total_1_abril} viajes del miércoles 1 de abril:")
print("\n   En el formulario del reporte de 'Viajes Completos':")
print(f"   📅 Fecha Inicio:  2026-04-01")
print(f"   📅 Fecha Fin:     2026-04-01")
print("\n   (O usa un rango más amplio como)")
print(f"   📅 Fecha Inicio:  2026-04-01")
print(f"   📅 Fecha Fin:     2026-04-06")

# Simular la query del reporte con diferentes rangos
print("\n" + "="*80)
print("SIMULACIÓN DE REPORTES CON DIFERENTES RANGOS")
print("="*80)

# Solo el 1 de abril
cursor.execute("""
    SELECT COUNT(*)
    FROM viajes
    WHERE fecha BETWEEN '2026-04-01' AND '2026-04-01'
""")
print(f"\n1️⃣  Rango: 2026-04-01 a 2026-04-01 → {cursor.fetchone()[0]} viajes")

# Toda la semana
cursor.execute("""
    SELECT COUNT(*)
    FROM viajes
    WHERE fecha BETWEEN '2026-04-01' AND '2026-04-06'
""")
print(f"2️⃣  Rango: 2026-04-01 a 2026-04-06 → {cursor.fetchone()[0]} viajes")

# Todo abril
cursor.execute("""
    SELECT COUNT(*)
    FROM viajes
    WHERE fecha BETWEEN '2026-04-01' AND '2026-04-30'
""")
print(f"3️⃣  Rango: 2026-04-01 a 2026-04-30 → {cursor.fetchone()[0]} viajes")

print("\n" + "="*80)
print("⚠️  IMPORTANTE")
print("="*80)
print("\nSi obtuviste solo 19 viajes en el reporte, probablemente usaste")
print("un rango de fechas ANTERIOR a la recuperación de datos.")
print("\nAsegúrate de incluir la fecha 2026-04-01 en tu rango de filtro.")

# Mostrar algunos viajes de ejemplo del 1 de abril para verificar
cursor.execute("""
    SELECT numero_viaje, conductor, casino
    FROM viajes
    WHERE fecha = '2026-04-01'
    ORDER BY id
    LIMIT 5
""")

print("\n📋 Primeros 5 viajes del 1 de abril (verificación):")
for num, conductor, casino in cursor.fetchall():
    print(f"   • Viaje {num} - {conductor} - {casino}")

conn.close()

print("\n" + "="*80)
print("✅ Usa estas fechas en el reporte y obtendrás todos los viajes")
print("="*80)
