import sqlite3
import os
import time

print("=" * 60)
print("REINICIANDO BASE DE DATOS COMPLETA")
print("=" * 60)

# Cerrar todas las conexiones WAL primero y renombrar BD antigua
db_path = 'viajes.db'
if os.path.exists(db_path):
    print(f"\nIntentando cerrar conexiones...")
    try:
        # Conectar y cerrar para forzar checkpoint
        temp_conn = sqlite3.connect(db_path, timeout=1)
        temp_conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        temp_conn.close()
        time.sleep(0.5)
    except Exception as e:
        print(f"Warning: {e}")
    
    print(f"\nMoviendo base de datos antigua...")
    try:
        # Renombrar en lugar de eliminar
        timestamp = int(time.time())
        for ext in ['', '-wal', '-shm']:
            old_file = db_path + ext
            if os.path.exists(old_file):
                new_file = f'viajes_backup_{timestamp}{ext}'
                try:
                    os.rename(old_file, new_file)
                except:
                    pass
        print("Base de datos antigua respaldada")
    except Exception as e:
        print(f"Warning: {e}")

# Crear nueva base de datos
print("\nCreando nueva base de datos...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Habilitar WAL mode
cursor.execute('PRAGMA journal_mode=WAL')

print("Creando tablas...")

# Tabla viajes con ID AUTOINCREMENT y UNIQUE constraint
cursor.execute('DROP TABLE IF EXISTS viajes')
cursor.execute('''
    CREATE TABLE viajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_viaje TEXT NOT NULL,
        casino TEXT,
        ruta TEXT,
        tipo_camion TEXT,
        patente_camion TEXT,
        patente_semi TEXT,
        numero_rampa TEXT,
        peso_camion TEXT,
        costo_codigo TEXT NOT NULL,
        termografos_gps TEXT,
        fecha TEXT,
        fecha_hora_llegada_dhl TEXT,
        fecha_hora_salida_dhl TEXT,
        conductor TEXT,
        celular TEXT,
        rut TEXT,
        numero_camion TEXT,
        num_wencos TEXT,
        bin TEXT,
        pallets TEXT,
        pallets_chep TEXT,
        pallets_pl_negro_grueso TEXT,
        pallets_pl_negro_alternativo TEXT,
        pallets_refrigerado TEXT,
        wencos_refrigerado TEXT,
        pallets_congelado TEXT,
        wencos_congelado TEXT,
        pallets_abarrote TEXT,
        check_congelado TEXT,
        check_refrigerado TEXT,
        check_abarrote TEXT,
        check_implementos TEXT,
        check_aseo TEXT,
        check_trazabilidad TEXT,
        check_plataforma_wtck TEXT,
        check_env_correo_wtck TEXT,
        check_revision_planilla_despacho TEXT,
        guia_1 TEXT,
        guia_2 TEXT,
        guia_3 TEXT,
        guia_4 TEXT,
        guia_5 TEXT,
        guia_6 TEXT,
        guia_7 TEXT,
        guia_8 TEXT,
        guia_9 TEXT,
        guia_10 TEXT,
        guia_11 TEXT,
        guia_12 TEXT,
        guia_13 TEXT,
        guia_14 TEXT,
        sello_salida_1p TEXT,
        sello_salida_2p TEXT,
        sello_salida_3p TEXT,
        sello_salida_4p TEXT,
        sello_salida_5p TEXT,
        sello_retorno_1p TEXT,
        sello_retorno_2p TEXT,
        sello_retorno_3p TEXT,
        sello_retorno_4p TEXT,
        sello_retorno_5p TEXT,
        numero_certificado_fumigacion TEXT,
        revision_limpieza_camion_acciones TEXT,
        administrativo_responsable TEXT,
        UNIQUE(numero_viaje, costo_codigo)
    )
''')
print("Tabla 'viajes' creada con ID AUTOINCREMENT y constraint UNIQUE(numero_viaje, costo_codigo)")

# Tabla comidas_preparadas
cursor.execute('DROP TABLE IF EXISTS comidas_preparadas')
cursor.execute('''
    CREATE TABLE comidas_preparadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_viaje TEXT NOT NULL,
        numero_centro_costo TEXT NOT NULL,
        guia_comida TEXT,
        descripcion TEXT,
        kilo REAL,
        bultos INTEGER,
        FOREIGN KEY (numero_viaje, numero_centro_costo) 
            REFERENCES viajes(numero_viaje, costo_codigo) ON DELETE CASCADE
    )
''')
print("Tabla 'comidas_preparadas' creada")

# Tabla maestras_casinos
cursor.execute('DROP TABLE IF EXISTS maestras_casinos')
cursor.execute('''
    CREATE TABLE maestras_casinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_centro_costo TEXT UNIQUE NOT NULL,
        nombre_casino TEXT NOT NULL,
        ruta TEXT
    )
''')
print("Tabla 'maestras_casinos' creada")

# Tabla maestras_choferes
cursor.execute('DROP TABLE IF EXISTS maestras_choferes')
cursor.execute('''
    CREATE TABLE maestras_choferes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        celular TEXT,
        rut TEXT
    )
''')
print("Tabla 'maestras_choferes' creada")

# Tabla maestras_administrativos
cursor.execute('DROP TABLE IF EXISTS maestras_administrativos')
cursor.execute('''
    CREATE TABLE maestras_administrativos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
''')
print("Tabla 'maestras_administrativos' creada")

print("\nPoblando maestras con datos básicos...")

# Poblar maestras_casinos con 3 registros de ejemplo
casinos = [
    ('100', 'ESTEBANDIDUSKUNFUCHICKEN', 'MAIPU'),
    ('200', 'CASINO CENTRAL', 'SANTIAGO'),
    ('300', 'CASINO SUR', 'PUENTE ALTO')
]
cursor.executemany('''
    INSERT INTO maestras_casinos (codigo_centro_costo, nombre_casino, ruta)
    VALUES (?, ?, ?)
''', casinos)
print(f"{len(casinos)} casinos agregados")

# Poblar maestras_choferes con 3 registros de ejemplo
choferes = [
    ('PATRICIO SOTO', '942906550', '13.628.536-K'),
    ('JUAN PEREZ', '912345678', '12.345.678-9'),
    ('MARIA GONZALEZ', '987654321', '11.222.333-4')
]
cursor.executemany('''
    INSERT INTO maestras_choferes (nombre, celular, rut)
    VALUES (?, ?, ?)
''', choferes)
print(f"{len(choferes)} choferes agregados")

# Poblar maestras_administrativos con 3 registros de ejemplo
administrativos = [
    ('LUCAS GNEMMI',),
    ('MARIA RODRIGUEZ',),
    ('CARLOS LOPEZ',)
]
cursor.executemany('''
    INSERT INTO maestras_administrativos (nombre)
    VALUES (?)
''', administrativos)
print(f"{len(administrativos)} administrativos agregados")

conn.commit()
conn.close()

print("\n" + "=" * 60)
print("BASE DE DATOS REINICIADA EXITOSAMENTE")
print("=" * 60)
print("\nResumen:")
print("   • Tabla viajes: ID AUTOINCREMENT + UNIQUE(numero_viaje, costo_codigo)")
print("   • Tabla comidas_preparadas: ID AUTOINCREMENT")
print("   • Maestras casinos: 3 registros")
print("   • Maestras choferes: 3 registros")
print("   • Maestras administrativos: 3 registros")
print("\n✨ La base de datos está lista para usar")
