import sqlite3

# Recrear tabla rendiciones sin columna rendicion_valor
conn = sqlite3.connect('viajes.db')
cursor = conn.cursor()

# Eliminar tabla si existe
cursor.execute('DROP TABLE IF EXISTS rendiciones')
print("✓ Tabla rendiciones eliminada (si existía)")

# Crear tabla nueva sin rendicion_valor
cursor.execute('''
CREATE TABLE rendiciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nro_viaje INTEGER UNIQUE NOT NULL,
    pdt TEXT,
    ruta TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME,
    estado_rendicion TEXT DEFAULT 'SIN REVISAR'
)
''')

conn.commit()
conn.close()

print("✓ Tabla rendiciones creada exitosamente (sin columna rendicion_valor)")
