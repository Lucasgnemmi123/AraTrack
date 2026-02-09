# Cómo Ver y Gestionar la Base de Datos

## Opción 1: DB Browser for SQLite (RECOMENDADO)

### Para ti (desarrollador):
1. Descarga DB Browser for SQLite Portable:
   - https://sqlitebrowser.org/dl/
   - Descargar "DB Browser for SQLite - PortableApp"
   
2. Extrae el .exe portable a la carpeta `AraTrack_Portable`

3. El usuario puede:
   - Abrir `DB.Browser.for.SQLite-xxx-win64.exe`
   - Click en "Abrir base de datos"
   - Seleccionar `viajes_dhl.db`
   - Ver/editar todas las tablas

### Para el usuario final:
- Usa DB Browser for SQLite si lo incluiste
- O descárgalo de: https://sqlitebrowser.org/dl/

## Opción 2: Desde la Aplicación (ya implementado)

Tu aplicación ya tiene acceso completo a los datos:
- **Ver viajes**: Formulario "Buscar Viaje"
- **Editar viajes**: Botón "Editar" en resultados
- **Reportes Excel**: Sección "Reportes" - descarga toda la data
- **Maestras**: Ver/editar casinos, choferes, administrativos

## Opción 3: Herramientas Simples

### Ver tablas rápidamente:
Crea un archivo `ver_tablas.py` al lado de `viajes_dhl.db`:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('viajes_dhl.db')

# Ver todas las tablas
print("TABLAS DISPONIBLES:")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for tabla in cursor.fetchall():
    print(f"  - {tabla[0]}")

# Ver datos de una tabla (ejemplo: viajes)
print("\nDATOS DE VIAJES (primeras 10 filas):")
df = pd.read_sql_query("SELECT * FROM viajes LIMIT 10", conn)
print(df)

conn.close()
```

Ejecutar: `python ver_tablas.py`

## Opción 4: Copiar la Base de Datos

Simplemente **copia** el archivo `viajes_dhl.db` desde `AraTrack_Portable` a tu máquina de desarrollo y ábrelo con cualquier herramienta SQLite.

## Resumen

**Más fácil para usuario NO técnico:**
- Incluye DB Browser portable en la carpeta

**Para ti (técnico):**
- Copia `viajes_dhl.db` y ábrela con tu herramienta favorita
- O usa los reportes Excel de la app

**Respaldo:**
- Siempre haz copia de `viajes_dhl.db` antes de modificar
