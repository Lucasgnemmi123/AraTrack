import sqlite3

conn = sqlite3.connect('viajes.db')
cursor = conn.cursor()

print("\n📋 TABLAS EN LA BASE DE DATOS:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()
for tabla in tablas:
    print(f"  - {tabla[0]}")

print("\n🔍 VERIFICANDO ESTRUCTURA DE TABLA casinos:")
cursor.execute("PRAGMA table_info(casinos)")
columnas = cursor.fetchall()
for col in columnas:
    print(f"  {col[1]} ({col[2]})")

conn.close()
