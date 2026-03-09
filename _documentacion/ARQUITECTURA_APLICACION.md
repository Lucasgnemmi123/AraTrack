# Arquitectura y Funcionamiento de la Aplicación

## Sistema de Viajes DHL - AraTrack

### Fecha: 27 de Febrero de 2026

---

## 1. VISIÓN GENERAL

**AraTrack** es un sistema web de gestión de viajes de transporte para DHL, diseñado para:
- Registrar y administrar viajes de distribución a casinos/centros de costo
- Gestionar comidas preparadas por viaje y centro de costo
- Generar PDFs de documentación de viajes
- Crear reportes Excel para facturación y control
- Gestionar rendiciones de viajes
- Administrar tablas maestras (choferes, casinos, administrativos, proveedores, transportes)

---

## 2. STACK TECNOLÓGICO

### Backend
- **Python 3.14**
- **Flask 3.0.0** - Framework web
- **Waitress 3.0.2** - Servidor WSGI de producción
- **SQLite 3** - Base de datos
- **ReportLab 4.0.9** - Generación de PDFs
- **Pandas 3.0.1** - Procesamiento de datos para reportes
- **OpenPyxl 3.1.5** - Generación de archivos Excel
- **psutil 5.9.0** - Gestión de procesos del sistema

### Frontend
- **HTML5 + Jinja2 Templates**
- **CSS3** (Bootstrap implícito)
- **JavaScript ES6+**
- **jQuery** - DOM manipulation y AJAX
- **Select2** - Selectores avanzados

### Gestión de Procesos
- **tkinter** - Interfaz gráfica para control del servidor
- **subprocess** - Gestión de procesos Python
- **threading** - Hilos para lectura de logs en tiempo real

---

## 3. ARQUITECTURA DE MÓDULOS

```
Sistema AraTrack
│
├── Módulo de Presentación (Frontend)
│   ├── Templates HTML (Jinja2)
│   ├── CSS Estático
│   └── JavaScript Cliente
│
├── Módulo de Aplicación (Backend)
│   ├── app_web.py              # Aplicación Flask principal
│   ├── auth_manager.py         # Autenticación y usuarios
│   ├── db_manager.py           # Gestión de base de datos
│   ├── maestras_manager.py     # Gestión tablas maestras
│   ├── rendiciones_manager.py  # Gestión de rendiciones
│   └── pdf_generator.py        # Generación de PDFs
│
├── Módulo de Configuración
│   └── config.py               # Configuración centralizada
│
├── Módulo de Control de Servidor
│   ├── servidor_gui.py         # Interfaz gráfica de control
│   └── SERVIDOR.bat            # Lanzador
│
└── Módulo de Datos
    └── viajes.db / viajes_dev.db  # Base de datos SQLite
```

---

## 4. COMPONENTES PRINCIPALES

### 4.1 app_web.py - Aplicación Principal

**Responsabilidades:**
- Inicialización de Flask y configuración
- Definición de todas las rutas HTTP
- Gestión de sesiones de usuario
- Coordinación entre módulos
- Manejo de errores HTTP

**Rutas Principales:**
- `/` - Dashboard principal
- `/login` - Autenticación
- `/nuevo-viaje` - Formulario de creación de viajes
- `/editar-viaje` - Edición de viajes existentes
- `/generar-pdf` - Interfaz de generación de PDFs
- `/reportes` - Panel de reportes Excel
- `/gestionar-usuarios` - Administración de usuarios
- `/dashboard` - Estadísticas y resumen

**APIs REST:**
- `/api/guardar-viaje` - Crear nuevo viaje
- `/api/actualizar-viaje` - Modificar viaje
- `/api/eliminar-viaje` - Eliminar viaje completo
- `/api/generar-pdf` - Generar PDF de viaje
- `/api/descargar-reporte-*` - Generación de reportes Excel
- `/api/maestras/*` - CRUD de tablas maestras

### 4.2 db_manager.py - Gestor de Base de Datos

**Responsabilidades:**
- Conexión y configuración SQLite
- Operaciones CRUD en tabla `viajes`
- Operaciones CRUD en tabla `comidas_preparadas`
- Gestión de transacciones
- Modo WAL para concurrencia

**Métodos Principales:**
```python
get_connection()                    # Conexión optimizada
insert_viaje(viaje_data)           # Insertar viaje
update_viaje(id, viaje_data)       # Actualizar viaje
delete_viaje(numero_viaje)         # Eliminar viaje
get_viaje_by_numero(numero_viaje)  # Obtener viaje
insert_comidas(comidas_data)       # Insertar comidas
get_comidas_by_viaje(numero_viaje) # Obtener comidas
```

**Configuración de Concurrencia:**
- `PRAGMA journal_mode=WAL` - Write-Ahead Logging
- `timeout=30.0` - Timeout de 30 segundos
- `busy_timeout=30000` - Espera hasta 30s en bloqueos
- `isolation_level=None` - Modo autocommit

### 4.3 maestras_manager.py - Gestor de Tablas Maestras

**Responsabilidades:**
- CRUD de choferes (nombre, RUT, celular)
- CRUD de casinos/centros de costo (código, nombre, ruta)
- CRUD de administrativos (nombre)
- Búsquedas y autocompletado
- Validación de duplicados

**Tablas Maestras:**
1. **maestras_choferes**: Conductores
2. **maestras_casinos**: Centros de costo / Destinos
3. **maestras_administrativos**: Personal administrativo
4. **proveedores**: Proveedores de comidas
5. **transportes**: Información de vehículos

**Métodos Principales:**
```python
# Búsquedas
buscar_choferes_por_nombre(nombre)
buscar_casino_por_codigo(codigo)
obtener_chofer_por_nombre(nombre)

# CRUD
crear_chofer(nombre, rut, celular)
actualizar_chofer(id, datos)
crear_casino(codigo, nombre, ruta)
actualizar_casino(id, datos)

# Listados
obtener_todos_los_choferes()
obtener_todos_casinos()
obtener_todos_los_administrativos()
```

### 4.4 pdf_generator.py - Generador de PDFs

**Responsabilidades:**
- Generación de PDFs de viajes
- Formato y diseño de documentos
- Inclusión de logos y firmas
- Tablas de comidas preparadas
- Checksums y validaciones

**Estructura del PDF:**
1. Encabezado con logo DHL
2. Información del viaje (número, fecha, casino)
3. Datos del transporte (patente, conductor, RUT)
4. Información de carga (pallets, wencos, bins)
5. Checklist de verificaciones
6. Tabla de comidas preparadas por centro de costo
7. Sellos de salida y retorno
8. Guías de despacho
9. Espacio para firmas (Conductor, Bodega, Receptor)

### 4.5 auth_manager.py - Gestor de Autenticación

**Responsabilidades:**
- Gestión de usuarios
- Hash de contraseñas (bcrypt)
- Validación de credenciales
- Creación y eliminación de usuarios
- Cambio de contraseñas

**Métodos Principales:**
```python
verificar_credenciales(username, password)
crear_usuario(username, password, nombre, email)
cambiar_password(username, nueva_password)
eliminar_usuario(user_id)
toggle_usuario_activo(user_id)
```

### 4.6 rendiciones_manager.py - Gestor de Rendiciones

**Responsabilidades:**
- Creación de rendiciones por viaje
- Actualización de estado (SIN REVISAR, APROBADO, RECHAZADO)
- Registro de PDT (Planilla de Transporte)
- Histórico de modificaciones

**Estados de Rendición:**
- `SIN REVISAR` - Rendición creada, pendiente de revisión
- `APROBADO` - Rendición aprobada
- `RECHAZADO` - Rendición rechazada, requiere corrección

### 4.7 servidor_gui.py - Interfaz Gráfica de Control

**Responsabilidades:**
- Inicio/detención del servidor web
- Visualización de logs en tiempo real
- Limpieza de procesos Python huérfanos
- Monitoreo de estado del servidor
- Protección de procesos propios

**Características:**
- Ventana tkinter con controles
- Log con colores (errores en rojo, éxitos en verde)
- Detección automática de servidor en ejecución
- Botones: Iniciar, Detener, Limpiar Procesos
- Cierre seguro con confirmación

---

## 5. FLUJO DE DATOS

### 5.1 Creación de Viaje

```
Usuario → Formulario Web
    ↓
Flask Router (/api/guardar-viaje)
    ↓
Validación de datos
    ↓
db_manager.insert_viaje()
    ↓
SQLite: INSERT INTO viajes
    ↓
db_manager.insert_comidas()
    ↓
SQLite: INSERT INTO comidas_preparadas
    ↓
maestras_manager (actualizar maestras si es nuevo)
    ↓
Respuesta JSON al cliente
    ↓
Actualización UI
```

### 5.2 Generación de PDF

```
Usuario → Interfaz Generar PDF
    ↓
Selección de Viaje + Centro de Costo
    ↓
Flask Router (/api/generar-pdf)
    ↓
db_manager.get_viaje_completo()
    ↓
db_manager.get_comidas_preparadas()
    ↓
pdf_generator.generar_pdf()
    ↓
ReportLab: Composición del documento
    ↓
Guardado en /pdfs/
    ↓
Respuesta con URL de descarga
    ↓
Cliente descarga PDF
```

### 5.3 Generación de Reportes Excel

```
Usuario → Panel de Reportes
    ↓
Selección de tipo de reporte + filtros
    ↓
Flask Router (/api/descargar-reporte-*)
    ↓
Lectura archivo SQL de queries/
    ↓
Ejecución de query en SQLite
    ↓
pandas.DataFrame(resultados)
    ↓
Aplicación de filtros y formato
    ↓
df.to_excel() con openpyxl
    ↓
Respuesta con archivo Excel
    ↓
Descarga automática en navegador
```

---

## 6. SEGURIDAD

### 6.1 Autenticación

- **Sesiones Flask**: `flask.session` con secret_key
- **Passwords hasheados**: bcrypt con salt automático
- **Login Required**: Decorator `@login_required` en rutas protegidas
- **Session timeout**: Sesión persiste hasta logout o cierre de navegador

### 6.2 Base de Datos

- **SQLite local**: No expuesta a red
- **Prepared statements**: Sin inyección SQL
- **WAL mode**: Múltiples lecturas simultáneas seguras
- **Backups automáticos**: Carpeta `_backups_bd/`

### 6.3 Archivos

- **PDFs en carpeta local**: `/pdfs/`
- **Acceso controlado**: Solo archivos solicitados explícitamente
- **Sin listado de directorios**: Seguridad por oscuridad

---

## 7. ESCALABILIDAD Y RENDIMIENTO

### 7.1 Concurrencia

- **Waitress**: Hasta 4 threads configurables
- **SQLite WAL**: Lecturas concurrentes ilimitadas, 1 escritura a la vez
- **Conexiones por request**: Patrón open-close en cada operación
- **Timeouts configurados**: 30 segundos para evitar deadlocks

### 7.2 Optimizaciones

- **Índices en SQLite**: Columnas `numero_viaje`, `costo_codigo`
- **PRAGMA optimizations**: `journal_mode=WAL`, `synchronous=NORMAL`
- **Carga lazy de tablas maestras**: Solo cuando se necesitan
- **Caché de Select2**: Reduce llamadas AJAX

### 7.3 Limitaciones Actuales

- **SQLite**: Máximo ~100 usuarios concurrentes recomendado
- **Escrituras secuenciales**: 1 escritura a la vez en BD
- **Sin caché Redis**: Cada request consulta BD
- **Sin CDN**: Assets servidos desde Flask

---

## 8. MANTENIMIENTO

### 8.1 Logs

- **Consola del servidor**: stdout/stderr capturados en GUI
- **Carpeta `_logs/`**: diagnostico.txt
- **Nivel de detalle**: Errores + Warnings por defecto

### 8.2 Backups

- **Base de datos**: `_backups_bd/viajes.db.backup_YYYYMMDD_HHMMSS`
- **Frecuencia**: Manual (recomendado diario)
- **Restauración**: Copiar backup sobre `viajes.db` con servidor detenido

### 8.3 Actualización del Sistema

1. Detener servidor (GUI o Ctrl+C)
2. Backup de `viajes.db`
3. Actualizar archivos Python
4. Ejecutar `RECREAR_ENTORNO.bat` si hay nuevas dependencias
5. Iniciar servidor con `SERVIDOR.bat`
6. Verificar funcionamiento

---

## 9. ENTORNO DE DESARROLLO vs PRODUCCIÓN

### Desarrollo
- Base de datos: `viajes_dev.db`
- Variable entorno: `ARATRACK_ENV=development`
- Debug mode: Activado (Flask)
- Servidor: Flask development server
- Puerto: 5000

### Producción
- Base de datos: `viajes.db`
- Variable entorno: `ARATRACK_ENV=production`
- Debug mode: Desactivado
- Servidor: Waitress WSGI
- Puerto: 5000
- Threads: 4

---

## 10. REFERENCIAS TÉCNICAS

### Documentos Relacionados
- `SERVIDOR_DOCUMENTACION.md` - Detalles del servidor Waitress
- `INTERFAZ_USO.md` - Guía de uso de la interfaz web
- `DIAGRAMA_FLUJO.md` - Diagramas de flujo de procesos
- `ESTRUCTURA_BD.md` - Esquema detallado de la base de datos

### Configuración Centralizada
Ver `config.py` para:
- Rutas de archivos
- Variables de entorno
- Configuración de threads
- Hosts y puertos

---

*Documento generado automáticamente el 27 de Febrero de 2026*
