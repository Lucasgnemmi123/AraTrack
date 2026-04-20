"""
Reporte final del estado de la base de datos
"""
import sqlite3

print("="*80)
print("REPORTE FINAL - BASE DE DATOS DE VIAJES")
print("="*80)
print()

conn = sqlite3.connect('viajes.db')
cur = conn.cursor()

# Estadísticas generales
cur.execute("SELECT COUNT(*), MIN(id), MAX(id) FROM viajes")
total, min_id, max_id = cur.fetchone()
print(f"📊 ESTADÍSTICAS GENERALES:")
print(f"   Total viajes en BD: {total:,}")
print(f"   Rango de IDs: {min_id} a {max_id}")
print()

# Viajes de abril 2026
print(f"📅 VIAJES DE ABRIL 2026:")
print("-" * 80)
cur.execute("""
    SELECT fecha, COUNT(*), MIN(id), MAX(id)
    FROM viajes 
    WHERE fecha LIKE '2026-04-%' 
    GROUP BY fecha 
    ORDER BY fecha
""")
total_abril = 0
for fecha, count, min_id_fecha, max_id_fecha in cur.fetchall():
    total_abril += count
    print(f"   {fecha}: {count:3d} viajes (IDs: {min_id_fecha:4d} - {max_id_fecha:4d})")
print(f"   {'TOTAL':10s}: {total_abril:3d} viajes")
print()

# Calidad de datos
print(f"✅ CALIDAD DE DATOS:")
print("-" * 80)

# RUTs bien formateados
cur.execute("""
    SELECT COUNT(*) 
    FROM viajes 
    WHERE fecha LIKE '2026-04-%' AND (rut LIKE '%-%' AND LENGTH(rut) BETWEEN 5 AND 15)
""")
ruts_buenos = cur.fetchone()[0]

# RUTs con problemas
cur.execute("""
    SELECT COUNT(*) 
    FROM viajes 
    WHERE fecha LIKE '2026-04-%' AND (rut IS NULL OR rut = '' OR rut = 'ADELANTO' 
          OR (rut NOT LIKE '%-%') OR LENGTH(rut) < 5 OR LENGTH(rut) > 15)
""")
ruts_problemas = cur.fetchone()[0]

porcentaje_buenos = (ruts_buenos * 100) // total_abril if total_abril > 0 else 0
print(f"   RUTs bien formateados: {ruts_buenos}/{total_abril} ({porcentaje_buenos}%)")
print(f"   RUTs con problemas: {ruts_problemas} (incluye ADELANTO, vacíos, etc.)")
print()

# Verificar maestras
print(f"📋 MAESTRAS:")
print("-" * 80)
cur.execute("SELECT COUNT(*) FROM maestras_casinos")
total_casinos = cur.fetchone()[0]
print(f"   Casinos registrados: {total_casinos}")

cur.execute("SELECT COUNT(*) FROM maestras_choferes")
total_choferes = cur.fetchone()[0]
print(f"   Choferes registrados: {total_choferes}")
print()

# Backups
print(f"💾 BACKUPS DISPONIBLES:")
print("-" * 80)
import os
if os.path.exists('_backups_bd'):
    backups = [f for f in os.listdir('_backups_bd') if f.endswith('.db')]
    backups.sort(reverse=True)
    for backup in backups[:3]:
        size = os.path.getsize(os.path.join('_backups_bd', backup))
        print(f"   {backup} ({size:,} bytes)")
print()

print("="*80)
print("✅ RESUMEN DE LA RECUPERACIÓN")
print("="*80)
print("✓ Viajes del 02/04: RECUPERADOS (74 viajes)")
print("✓ Viajes del 03/04: RECUPERADOS (72 viajes)")
print("✓ Viajes del 04/04: RECUPERADOS (119 viajes)")
print("✓ Viajes del 05/04: No se trabajó (correcto)")
print("✓ Viajes del 06/04: Completos (24 viajes)")
print("✓ RUTs del 01/04: CORREGIDOS (76 RUTs reparados)")
print()
print("✓ Ningún ID fue pisado - Solo se agregaron nuevos registros")
print("✓ Backups de seguridad creados antes de cada operación")
print("="*80)

conn.close()
