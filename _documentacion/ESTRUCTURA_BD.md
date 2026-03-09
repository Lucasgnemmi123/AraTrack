# Estructura Relacional de la Base de Datos

## Sistema de Viajes DHL - Esquema de Base de Datos SQLite

### Fecha: 27 de Febrero de 2026

---

## 1. VISIÓN GENERAL

**Motor de Base de Datos**: SQLite 3  
**Archivo de Producción**: `viajes.db`  
**Archivo de Desarrollo**: `viajes_dev.db`  
**Modo de Concurrencia**: WAL (Write-Ahead Logging)  
**Encoding**: UTF-8

### Tablas Principales

| Tabla | Descripción | Registros Típicos |
|-------|-------------|-------------------|
| **viajes** | Información completa de cada viaje | 1000-10000 |
| **comidas_preparadas** | Comidas por viaje y centro de costo | 5000-50000 |
| **maestras_choferes** | Catálogo de conductores | 50-200 |
| **maestras_casinos** | Catálogo de centros de costo/casinos | 100-500 |
| **maestras_administrativos** | Catálogo de personal administrativo | 20-100 |
| **proveedores** | Catálogo de proveedores de comidas | 10-50 |
| **transportes** | Información de vehículos | 50-200 |
| **usuarios** | Usuarios del sistema | 5-50 |
| **rendiciones** | Estado de rendiciones de viajes | 1000-10000 |

---

## 2. TABLA: viajes

### Descripción
Tabla principal que almacena toda la información de cada viaje de transporte. Cada registro representa un viaje completo con todos sus detalles.

### Estructura

```sql
CREATE TABLE viajes (
    -- Identificación
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_viaje TEXT NOT NULL,
    
    -- Destino
    casino TEXT,
    ruta TEXT,
    costo_codigo TEXT NOT NULL,
    
    -- Transporte
    tipo_camion TEXT,
    patente_camion TEXT,
    patente_semi TEXT,
    numero_rampa TEXT,
    peso_camion TEXT,
    transporte TEXT,
    termografos_gps TEXT,
    
    -- Fechas
    fecha TEXT,
    fecha_hora_llegada_dhl TEXT,
    fecha_hora_salida_dhl TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Conductor
    conductor TEXT,
    celular TEXT,
    rut TEXT,
    numero_camion TEXT,
    
    -- Carga - Pallets
    pallets INTEGER DEFAULT 0,
    pallets_chep INTEGER DEFAULT 0,
    pallets_pl_negro_grueso INTEGER DEFAULT 0,
    pallets_pl_negro_alternativo INTEGER DEFAULT 0,
    pallets_plastico INTEGER DEFAULT 0,
    pallets_refrigerado INTEGER DEFAULT 0,
    pallets_congelado INTEGER DEFAULT 0,
    pallets_abarrote INTEGER DEFAULT 0,
    
    -- Carga - Wencos y Bins
    num_wencos INTEGER DEFAULT 0,
    wencos_refrigerado INTEGER DEFAULT 0,
    wencos_congelado INTEGER DEFAULT 0,
    bin INTEGER DEFAULT 0,
    
    -- Checklist de Verificación
    check_congelado INTEGER DEFAULT 0,
    check_refrigerado INTEGER DEFAULT 0,
    check_abarrote INTEGER DEFAULT 0,
    check_implementos INTEGER DEFAULT 0,
    check_aseo INTEGER DEFAULT 0,
    check_trazabilidad INTEGER DEFAULT 0,
    check_plataforma_wtck INTEGER DEFAULT 0,
    check_env_correo_wtck INTEGER DEFAULT 0,
    check_revision_planilla_despacho INTEGER DEFAULT 0,
    
    -- Sellos de Seguridad - Salida
    sello_salida_1p TEXT,
    sello_salida_2p TEXT,
    sello_salida_3p TEXT,
    sello_salida_4p TEXT,
    sello_salida_5p TEXT,
    
    -- Sellos de Seguridad - Retorno
    sello_retorno_1p TEXT,
    sello_retorno_2p TEXT,
    sello_retorno_3p TEXT,
    sello_retorno_4p TEXT,
    sello_retorno_5p TEXT,
    
    -- Guías de Despacho (21 campos)
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
    guia_15 TEXT,
    guia_16 TEXT,
    guia_17 TEXT,
    guia_18 TEXT,
    guia_19 TEXT,
    guia_20 TEXT,
    guia_21 TEXT,
    
    -- Certificaciones y Observaciones
    numero_certificado_fumigacion TEXT,
    revision_limpieza_camion_acciones TEXT,
    administrativo_responsable TEXT
);
```

### Índices

```sql
CREATE INDEX idx_viajes_numero ON viajes(numero_viaje);
CREATE INDEX idx_viajes_centro ON viajes(costo_codigo);
CREATE INDEX idx_viajes_fecha ON viajes(fecha);
CREATE INDEX idx_viajes_conductor ON viajes(conductor);
CREATE INDEX idx_viajes_created ON viajes(created_at);
```

### Constraints

- **PRIMARY KEY**: `id`
- **NOT NULL**: `numero_viaje`, `costo_codigo`
- **UNIQUE**: Ninguno (se permiten múltiples registros por número de viaje si tienen distintos centros de costo)

### Relaciones

- **1:N** con `comidas_preparadas` (un viaje puede tener muchas comidas)
- **N:1** con `maestras_casinos` (referencia a `costo_codigo`)
- **N:1** con `maestras_choferes` (referencia a `conductor`)
- **N:1** con `maestras_administrativos` (referencia a `administrativo_responsable`)
- **1:1** con `rendiciones` (un viaje puede tener una rendición)

### Tipos de Datos

| Columna | Tipo | Rango/Formato | Ejemplo |
|---------|------|---------------|---------|
| id | INTEGER | 1-∞ | 1, 2, 3... |
| numero_viaje | TEXT | Alfanumérico | V-2026-001 |
| fecha | TEXT | DD/MM/YYYY | 27/02/2026 |
| fecha_hora_llegada_dhl | TEXT | DD/MM/YYYY HH:MM | 27/02/2026 08:30 |
| conductor | TEXT | Nombre completo | Pedro González |
| rut | TEXT | NN.NNN.NNN-D | 12.345.678-9 |
| celular | TEXT | +56NNNNNNNNN | +56912345678 |
| pallets | INTEGER | 0-9999 | 120 |
| check_* | INTEGER | 0 o 1 (boolean) | 1 |

### Valores por Defecto

- Campos numéricos: `0`
- Campos de texto: `NULL` o vacío
- `created_at`: `CURRENT_TIMESTAMP`

---

## 3. TABLA: comidas_preparadas

### Descripción
Tabla relacionada que almacena las comidas transportadas en cada viaje, agrupadas por centro de costo.

### Estructura

```sql
CREATE TABLE comidas_preparadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_viaje TEXT NOT NULL,
    numero_centro_costo TEXT NOT NULL,
    guia_comida TEXT,
    descripcion TEXT,
    kilo REAL,
    bultos INTEGER,
    proveedor TEXT,
    
    -- Foreign Keys
    FOREIGN KEY (numero_viaje, numero_centro_costo) 
        REFERENCES viajes(numero_viaje, costo_codigo) 
        ON DELETE CASCADE
);
```

### Índices

```sql
CREATE INDEX idx_comidas_viaje ON comidas_preparadas(numero_viaje);
CREATE INDEX idx_comidas_centro ON comidas_preparadas(numero_centro_costo);
CREATE INDEX idx_comidas_proveedor ON comidas_preparadas(proveedor);
```

### Constraints

- **PRIMARY KEY**: `id`
- **NOT NULL**: `numero_viaje`, `numero_centro_costo`
- **FOREIGN KEY**: `(numero_viaje, numero_centro_costo)` referencia `viajes`
- **ON DELETE CASCADE**: Al eliminar un viaje, se eliminan sus comidas

### Relaciones

- **N:1** con `viajes` (muchas comidas pertenecen a un viaje)
- **N:1** con `proveedores` (referencia a `proveedor`)

### Campos Detallados

| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| id | Identificador único | INTEGER | 1 |
| numero_viaje | Número del viaje padre | TEXT | V-2026-001 |
| numero_centro_costo | Centro de costo destino | TEXT | 12345 |
| guia_comida | Número de guía de la comida | TEXT | GC-2026-500 |
| descripcion | Descripción del producto | TEXT | Pollo asado |
| kilo | Peso en kilogramos | REAL | 50.5 |
| bultos | Cantidad de bultos/cajas | INTEGER | 10 |
| proveedor | Nombre del proveedor | TEXT | Proveedor ABC |

---

## 4. TABLA: maestras_choferes

### Descripción
Catálogo de conductores registrados en el sistema.

### Estructura

```sql
CREATE TABLE maestras_choferes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    rut TEXT UNIQUE NOT NULL,
    celular TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices

```sql
CREATE UNIQUE INDEX idx_choferes_rut ON maestras_choferes(rut);
CREATE INDEX idx_choferes_nombre ON maestras_choferes(nombre);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `nombre`, `rut`
- **NOT NULL**: `nombre`, `rut`

### Relaciones

- **1:N** con `viajes` (un chofer puede hacer muchos viajes)

---

## 5. TABLA: maestras_casinos

### Descripción
Catálogo de centros de costo (casinos/destinos) del sistema.

### Estructura

```sql
CREATE TABLE maestras_casinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_costo INTEGER UNIQUE NOT NULL,
    casino TEXT NOT NULL,
    ruta TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices

```sql
CREATE UNIQUE INDEX idx_casinos_codigo ON maestras_casinos(codigo_costo);
CREATE INDEX idx_casinos_nombre ON maestras_casinos(casino);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `codigo_costo`
- **NOT NULL**: `codigo_costo`, `casino`

### Relaciones

- **1:N** con `viajes` (un casino puede recibir muchos viajes)

---

## 6. TABLA: maestras_administrativos

### Descripción
Catálogo de personal administrativo responsable de viajes.

### Estructura

```sql
CREATE TABLE maestras_administrativos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `nombre`
- **NOT NULL**: `nombre`

### Relaciones

- **1:N** con `viajes` (un administrativo puede ser responsable de muchos viajes)

---

## 7. TABLA: proveedores

### Descripción
Catálogo de proveedores de comidas preparadas.

### Estructura

```sql
CREATE TABLE proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `nombre`
- **NOT NULL**: `nombre`

### Relaciones

- **1:N** con `comidas_preparadas` (un proveedor puede suministrar muchas comidas)

---

## 8. TABLA: transportes

### Descripción
Catálogo de vehículos de transporte.

### Estructura

```sql
CREATE TABLE transportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patente TEXT UNIQUE NOT NULL,
    tipo TEXT,
    empresa TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `patente`
- **NOT NULL**: `patente`

### Relaciones

- **1:N** con `viajes` (un transporte puede hacer muchos viajes)

---

## 9. TABLA: usuarios

### Descripción
Usuarios del sistema web con autenticación.

### Estructura

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    email TEXT,
    activo INTEGER DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices

```sql
CREATE UNIQUE INDEX idx_usuarios_username ON usuarios(username);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `username`
- **NOT NULL**: `username`, `password_hash`, `nombre_completo`
- **DEFAULT**: `activo = 1`

### Campos Detallados

| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| id | Identificador único | INTEGER | 1 |
| username | Nombre de usuario (login) | TEXT | admin |
| password_hash | Hash SHA-256 de la contraseña | TEXT | a665a45920422f9d417e... |
| nombre_completo | Nombre real del usuario | TEXT | Juan Pérez |
| email | Correo electrónico (opcional) | TEXT | juan@dhl.com |
| activo | Estado (1=activo, 0=inactivo) | INTEGER | 1 |
| fecha_creacion | Fecha de creación del usuario | TIMESTAMP | 2026-02-27 10:00:00 |

### Seguridad

- Passwords hasheados con **SHA-256** (256 bits)
- **No se almacenan contraseñas en texto plano**
- Campo `activo` permite deshabilitar usuarios sin eliminarlos

---

## 10. TABLA: rendiciones

### Descripción
Estado de rendiciones (documentación administrativa) de viajes.

### Estructura

```sql
CREATE TABLE rendiciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nro_viaje INTEGER UNIQUE NOT NULL,
    pdt TEXT,
    ruta TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion DATETIME,
    estado_rendicion TEXT DEFAULT 'SIN REVISAR'
);
```

### Índices

```sql
CREATE UNIQUE INDEX idx_rendiciones_viaje ON rendiciones(nro_viaje);
CREATE INDEX idx_rendiciones_estado ON rendiciones(estado_rendicion);
```

### Constraints

- **PRIMARY KEY**: `id`
- **UNIQUE**: `nro_viaje`
- **NOT NULL**: `nro_viaje`
- **DEFAULT**: `estado_rendicion = 'SIN REVISAR'`

### Estados Posibles

| Estado | Descripción |
|--------|-------------|
| SIN REVISAR | Rendición creada, pendiente de revisión |
| APROBADO | Rendición aprobada por administración |
| RECHAZADO | Rendición rechazada, requiere corrección |

### Relaciones

- **1:1** con `viajes` (un viaje tiene una rendición)

---

## 11. DIAGRAMA ENTIDAD-RELACIÓN (ER)

### TABLAS Y SUS RELACIONES

#### Tabla Central: **viajes**
La tabla principal que conecta todo el sistema.

**Campos principales:**
- id (PK)
- numero_viaje
- costo_codigo
- conductor
- administrativo_responsable
- fecha, patente_camion, tipo_camion
- 60+ campos totales

#### Tablas Relacionadas Directamente con VIAJES:

| Tabla | Relación | Tipo | Campos Clave |
|-------|----------|------|-------------|
| **comidas_preparadas** | viajes → comidas | 1:N | FK: numero_viaje, numero_centro_costo |
| **rendiciones** | viajes → rendiciones | 1:1 | FK: nro_viaje |
| **maestras_casinos** | viajes ← casinos | N:1 | Referencia: costo_codigo |
| **maestras_choferes** | viajes ← choferes | N:1 | Referencia: conductor |
| **maestras_administrativos** | viajes ← admins | N:1 | Referencia: administrativo_responsable |
| **transportes** | viajes ← transportes | N:1 | Referencia: patente_camion |

#### Tablas Relacionadas Indirectamente:

| Tabla | Relación | Tipo | Campos Clave |
|-------|----------|------|-------------|
| **proveedores** | comidas ← proveedores | N:1 | Referencia: proveedor |

#### Tabla Independiente:

| Tabla | Descripción |
|-------|-------------|
| **usuarios** | Sistema de autenticación, sin relaciones directas con viajes |

### FLUJO DE DATOS

**Creación de un viaje completo:**
1. Usuario inicia sesión (**usuarios**)
2. Selecciona datos de **maestras_choferes**, **maestras_casinos**, **maestras_administrativos**
3. Crea registro en **viajes** (tabla central)
4. Agrega comidas en **comidas_preparadas** (1:N con viajes)
5. Sistema registra en **rendiciones** (1:1 con viajes)

**LEYENDA:**
- **PK** = Primary Key (Clave Primaria)
- **FK** = Foreign Key (Clave Foránea)
- **U** = Unique (Único)
- **1:N** = Uno a Muchos
- **N:1** = Muchos a Uno
- **1:1** = Uno a Uno

---

## 12. CARDINALIDAD DE RELACIONES

| Tabla Origen | Relación | Tabla Destino | Cardinalidad | ON DELETE |
|--------------|----------|---------------|--------------|-----------|
| viajes | tiene | comidas_preparadas | 1:N | CASCADE |
| viajes | pertenece a | maestras_casinos | N:1 | - |
| viajes | conducido por | maestras_choferes | N:1 | - |
| viajes | responsable | maestras_administrativos | N:1 | - |
| viajes | usa | transportes | N:1 | - |
| viajes | tiene | rendiciones | 1:1 | - |
| comidas_preparadas | suministrado por | proveedores | N:1 | - |

**Nota sobre CASCADE:**
- Solo `comidas_preparadas` tiene **ON DELETE CASCADE**
- Al eliminar un viaje, todas sus comidas se eliminan automáticamente
- Maestras (choferes, casinos, etc.) NO se eliminan en cascada

---

## 13. INTEGRIDAD REFERENCIAL

### Reglas Implementadas

1. **viajes.costo_codigo → maestras_casinos.codigo_costo**
   - Validación a nivel de aplicación (no FOREIGN KEY física)
   - Se permite "orphans" si el casino se elimina

2. **viajes.conductor → maestras_choferes.nombre**
   - Validación a nivel de aplicación
   - Se permite texto libre si chofer no está en maestras

3. **comidas_preparadas.(numero_viaje, numero_centro_costo) → viajes**
   - FOREIGN KEY con ON DELETE CASCADE
   - Eliminación en cascada garantizada

4. **comidas_preparadas.proveedor → proveedores.nombre**
   - Validación a nivel de aplicación
   - Se permite texto libre

### Validaciones en Código

```python
# En db_manager.py y maestras_manager.py:
- Verificación de duplicados (RUT, username, codigo_costo)
- Autocompletado para usar datos de maestras
- Creación automática de maestras si no existen
- Validación de formato (RUT, fechas, números)
```

---

## 14. OPTIMIZACIONES

### Índices Creados

```sql
-- Viajes
CREATE INDEX idx_viajes_numero ON viajes(numero_viaje);
CREATE INDEX idx_viajes_centro ON viajes(costo_codigo);
CREATE INDEX idx_viajes_fecha ON viajes(fecha);
CREATE INDEX idx_viajes_conductor ON viajes(conductor);
CREATE INDEX idx_viajes_created ON viajes(created_at);

-- Comidas Preparadas
CREATE INDEX idx_comidas_viaje ON comidas_preparadas(numero_viaje);
CREATE INDEX idx_comidas_centro ON comidas_preparadas(numero_centro_costo);
CREATE INDEX idx_comidas_proveedor ON comidas_preparadas(proveedor);

-- Maestras
CREATE UNIQUE INDEX idx_choferes_rut ON maestras_choferes(rut);
CREATE INDEX idx_choferes_nombre ON maestras_choferes(nombre);
CREATE UNIQUE INDEX idx_casinos_codigo ON maestras_casinos(codigo_costo);
CREATE INDEX idx_casinos_nombre ON maestras_casinos(casino);

-- Usuarios
CREATE UNIQUE INDEX idx_usuarios_username ON usuarios(username);

-- Rendiciones
CREATE UNIQUE INDEX idx_rendiciones_viaje ON rendiciones(nro_viaje);
CREATE INDEX idx_rendiciones_estado ON rendiciones(estado_rendicion);
```

### PRAGMAs de Optimización

```sql
PRAGMA journal_mode=WAL;           -- Concurrencia de lecturas
PRAGMA synchronous=NORMAL;         -- Balance seguridad/velocidad
PRAGMA cache_size=10000;           -- 10MB de caché
PRAGMA temp_store=MEMORY;          -- Temporales en RAM
PRAGMA busy_timeout=30000;         -- Timeout de 30s
PRAGMA foreign_keys=ON;            -- Habilitar FKs
```

---

## 15. QUERIES COMUNES OPTIMIZADAS

### Buscar Viaje Completo con Comidas

```sql
SELECT 
    v.*,
    GROUP_CONCAT(
        c.descripcion || ' (' || c.kilo || 'kg)', 
        ', '
    ) as comidas
FROM viajes v
LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje 
    AND v.costo_codigo = c.numero_centro_costo
WHERE v.numero_viaje = 'V-2026-001'
    AND v.costo_codigo = '12345'
GROUP BY v.id;
```

### Reporte de Facturación por Centro de Costo

```sql
SELECT 
    v.costo_codigo,
    mc.casino,
    COUNT(DISTINCT v.numero_viaje) as total_viajes,
    SUM(v.pallets) as total_pallets,
    SUM(v.num_wencos) as total_wencos,
    SUM(c.kilo) as total_kilos_comida
FROM viajes v
LEFT JOIN maestras_casinos mc ON v.costo_codigo = CAST(mc.codigo_costo AS TEXT)
LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje
WHERE v.fecha BETWEEN '01/02/2026' AND '28/02/2026'
GROUP BY v.costo_codigo, mc.casino
ORDER BY total_viajes DESC;
```

### Viajes por Conductor

```sql
SELECT 
    v.conductor,
    mch.rut,
    mch.celular,
    COUNT(v.id) as total_viajes,
    MIN(v.fecha) as primer_viaje,
    MAX(v.fecha) as ultimo_viaje
FROM viajes v
LEFT JOIN maestras_choferes mch ON v.conductor = mch.nombre
GROUP BY v.conductor
ORDER BY total_viajes DESC;
```

### Comidas por Proveedor

```sql
SELECT 
    c.proveedor,
    COUNT(c.id) as total_entregas,
    SUM(c.kilo) as total_kilos,
    SUM(c.bultos) as total_bultos,
    COUNT(DISTINCT c.numero_viaje) as viajes_atendidos
FROM comidas_preparadas c
WHERE c.proveedor IS NOT NULL AND c.proveedor != ''
GROUP BY c.proveedor
ORDER BY total_kilos DESC;
```

---

## 16. MANTENIMIENTO Y BACKUP

### Backup Automático

```bash
# Estructura de backups
_backups_bd/
  └── viajes.db.backup_YYYYMMDD_HHMMSS
      viajes.db.backup_20260227_100000
      viajes.db.backup_20260226_150000
      ...
```

### Comando de Backup

```bash
# Desde PowerShell o CMD:
copy viajes.db "_backups_bd\viajes.db.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
```

### Restauración desde Backup

```bash
# 1. Detener servidor (SERVIDOR.bat → Detener)
# 2. Restaurar backup:
copy "_backups_bd\viajes.db.backup_20260227_100000" viajes.db
# 3. Iniciar servidor
```

### Optimización de Base de Datos

```sql
-- Ejecutar periódicamente (mensualmente):
VACUUM;              -- Compactar BD y liberar espacio
ANALYZE;             -- Actualizar estadísticas de índices
REINDEX;             -- Reconstruir índices
```

### Verificación de Integridad

```sql
PRAGMA integrity_check;
-- Resultado esperado: "ok"

PRAGMA foreign_key_check;
-- Resultado esperado: 0 rows (sin errores)
```

---

## 17. ESTADÍSTICAS Y TAMAÑO

### Tamaño Estimado por Tabla

| Tabla | Registros | Tamaño Promedio/Registro | Tamaño Total Estimado |
|-------|-----------|--------------------------|----------------------|
| viajes | 5,000 | 2 KB | ~10 MB |
| comidas_preparadas | 25,000 | 500 bytes | ~12 MB |
| maestras_choferes | 100 | 200 bytes | ~20 KB |
| maestras_casinos | 300 | 200 bytes | ~60 KB |
| maestras_administrativos | 50 | 100 bytes | ~5 KB |
| proveedores | 30 | 100 bytes | ~3 KB |
| transportes | 150 | 200 bytes | ~30 KB |
| usuarios | 20 | 300 bytes | ~6 KB |
| rendiciones | 5,000 | 300 bytes | ~1.5 MB |
| **TOTAL** | | | **~24 MB** |

### Crecimiento Anual Estimado

- **Viajes nuevos/año**: ~3,000
- **Comidas nuevas/año**: ~15,000
- **Crecimiento/año**: ~14 MB
- **Tamaño en 5 años**: ~100 MB

**Conclusión**: SQLite es adecuado para este volumen de datos durante muchos años.

---

## 18. MIGRACIÓN Y EVOLUCIÓN

### Agregar Nueva Columna

```sql
-- Ejemplo: Agregar campo "observaciones" a viajes
ALTER TABLE viajes ADD COLUMN observaciones TEXT;
```

**Nota**: SQLite no permite eliminar columnas. Para eliminar, crear nueva tabla y migrar datos.

### Migrar a PostgreSQL (Futuro)

```python
# Script de migración (conceptual):
import sqlite3
import psycopg2

# 1. Exportar de SQLite
conn_sqlite = sqlite3.connect('viajes.db')
data = conn_sqlite.execute('SELECT * FROM viajes').fetchall()

# 2. Importar a PostgreSQL
conn_pg = psycopg2.connect(...)
conn_pg.executemany('INSERT INTO viajes VALUES (...)', data)
```

---

## 19. SEGURIDAD DE DATOS

### Nivel de Seguridad Actual

✅ **Implementado:**
- Passwords hasheados (SHA-256)
- Sesiones cifradas en servidor
- Sin inyección SQL (uso de prepared statements)
- Base de datos local (no expuesta a internet)

❌ **No Implementado (mejoras futuras):**
- Encriptación de base de datos en disco
- Audit log de cambios
- Versionado de registros
- Soft delete (borrado lógico)

### Recomendaciones

1. **Backups diarios automáticos**
2. **Encriptación de backups** si contienen datos sensibles
3. **Control de acceso** al archivo `viajes.db`
4. **Audit log** para rastrear quién modificó qué

---

## 20. REFERENCIAS

### Documentos Relacionados
- `ARQUITECTURA_APLICACION.md` - Detalles de la aplicación
- `SERVIDOR_DOCUMENTACION.md` - Configuración del servidor
- `INTERFAZ_USO.md` - Guía de uso de la interfaz
- `DIAGRAMAS_FLUJO.md` - Diagramas de procesos

### Archivos de Código
- `db_manager.py` - Lógica de acceso a datos
- `maestras_manager.py` - Gestión de tablas maestras
- `auth_manager.py` - Gestión de usuarios
- `rendiciones_manager.py` - Gestión de rendiciones

### Consultas SQL de Reportes
- `queries/` - Carpeta con queries .sql para reportes
- `queries/README.md` - Documentación de queries

---

*Documento generado automáticamente el 27 de Febrero de 2026*
