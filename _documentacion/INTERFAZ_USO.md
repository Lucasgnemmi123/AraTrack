# Guía de Uso de la Interfaz Web

## Sistema de Viajes DHL - Manual de Usuario

### Fecha: 27 de Febrero de 2026

---

## 1. ACCESO AL SISTEMA

### 1.1 Iniciar el Servidor

**Opción 1: Interfaz Gráfica (Recomendado)**
1. Hacer doble clic en `SERVIDOR.bat`
2. Se abrirá la ventana de control del servidor
3. Click en **▶ INICIAR SERVIDOR**
4. Esperar mensaje: "El servidor estará disponible en..."

**Opción 2: Línea de Comandos**
1. Abrir CMD en la carpeta del proyecto
2. Ejecutar: `iniciar_web.bat`
3. Esperar las URLs de acceso

### 1.2 Abrir el Navegador

**Desde la misma PC:**
- Abrir navegador (Chrome, Firefox, Edge)
- Ir a: `http://localhost:5000`

**Desde otra PC en la red:**
- Abrir navegador
- Ir a: `http://[IP-SERVIDOR]:5000`
- Ejemplo: `http://192.168.1.100:5000`

### 1.3 Iniciar Sesión

```
Usuario por defecto: admin
Contraseña: admin123
```

**Pantalla de Login:**
- Campo "Usuario"
- Campo "Contraseña"
- Botón "Iniciar Sesión"

⚠️ **Importante**: Cambiar contraseña después del primer acceso.

---

## 2. NAVEGACIÓN PRINCIPAL

### 2.1 Barra de Navegación Superior

```
[Logo DHL]  Inicio | Nuevo Viaje | Editar Viaje | Generar PDF | Reportes | Dashboard | Usuarios | Salir
```

**Elementos:**
- **Inicio**: Dashboard principal con estadísticas
- **Nuevo Viaje**: Crear un nuevo registro de viaje
- **Editar Viaje**: Modificar o eliminar viajes existentes
- **Generar PDF**: Crear documentos PDF de viajes
- **Reportes**: Descargar reportes en Excel
- **Dashboard**: Estadísticas y gráficos
- **Usuarios**: Gestión de usuarios (solo admin)
- **Salir**: Cerrar sesión

### 2.2 Dashboard (Pantalla Principal)

**Secciones:**
1. **Estadísticas Generales**
   - Total de viajes registrados
   - Viajes del mes actual
   - Centros de costo activos
   - Conductores registrados

2. **Viajes Recientes**
   - Tabla con últimos 10 viajes
   - Columnas: Número, Casino, Fecha, Conductor, Acciones

3. **Accesos Rápidos**
   - Botones para funciones principales
   - Links directos a formularios

---

## 3. CREAR NUEVO VIAJE

### 3.1 Acceso al Formulario

**Ruta**: Navegación → Nuevo Viaje → `/nuevo-viaje`

### 3.2 Secciones del Formulario

#### A. Información Básica del Viaje

| Campo | Descripción | Requerido | Ejemplo |
|-------|-------------|-----------|---------|
| Número de Viaje | Identificador único del viaje | ✅ Sí | V-2026-001 |
| Fecha | Fecha del viaje | ✅ Sí | 27/02/2026 |
| Centro de Costo | Código del destino | ✅ Sí | 12345 |
| Casino | Nombre del casino/destino | ✅ Sí | Casino Central |
| Ruta | Descripción de la ruta | ❌ No | Santiago - Valparaíso |
| Administrativo Responsable | Nombre del responsable | ✅ Sí | Juan Pérez |

**Autocompletado:**
- **Centro de Costo**: Muestra casino y ruta automáticamente
- **Casino**: Busca en maestras_casinos
- **Administrativo**: Lista de maestras_administrativos

#### B. Información del Transporte

| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| Tipo de Camión | Tipo de vehículo | Select | Refrigerado |
| Patente Camión | Placa del camión | Text | ABCD12 |
| Patente Semi | Placa del semirremolque | Text | XYZ789 |
| Número de Rampa | Número de rampa asignado | Text | R-05 |
| Transporte | Nombre de la empresa | Text | Transportes ABC |
| Termógrafos/GPS | Código de dispositivos | Text | GPS-001, TEMP-002 |

**Select "Tipo de Camión":**
- Refrigerado
- Congelado
- Mixto
- Abarrote
- Otro

#### C. Información del Conductor

| Campo | Descripción | Autocompletado | Ejemplo |
|-------|-------------|----------------|---------|
| Conductor | Nombre completo | ✅ Sí | Pedro González |
| RUT | RUT del conductor | ✅ Sí | 12.345.678-9 |
| Celular | Teléfono | ✅ Sí | +56912345678 |

**Funcionamiento del Autocompletado:**
1. Escribir nombre del conductor
2. Aparecen sugerencias desde `maestras_choferes`
3. Seleccionar conductor
4. RUT y Celular se llenan automáticamente

**Si conductor no existe:**
- Se puede escribir manualmente
- Sistema preguntará si agregarlo a maestras al guardar

#### D. Fechas de Operación

| Campo | Descripción | Formato | Ejemplo |
|-------|-------------|---------|---------|
| Fecha/Hora Llegada DHL | Llegada a bodega DHL | DD/MM/YYYY HH:MM | 27/02/2026 08:30 |
| Fecha/Hora Salida DHL | Salida de bodega DHL | DD/MM/YYYY HH:MM | 27/02/2026 10:45 |

**Nota**: Usar formato 24 horas.

#### E. Información de Carga

**Pallets:**
| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| Cantidad Pallets | Total de pallets | Number | 120 |
| Pallets CHEP | Pallets azules CHEP | Number | 80 |
| Pallets PL Negro Grueso | Pallets negros gruesos | Number | 20 |
| Pallets PL Negro Alternativo | Otros pallets negros | Number | 10 |
| Pallets Plásticos | Pallets de plástico | Number | 10 |

**Wencos:**
| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| N° Wencos | Cantidad de bins/bateas | Number | 50 |
| Bins | Cantidad de bins | Number | 30 |

**Por Tipo de Carga:**
| Tipo | Pallets | Wencos |
|------|---------|--------|
| Refrigerado | Pallets Refrigerado | Wencos Refrigerado |
| Congelado | Pallets Congelado | Wencos Congelado |
| Abarrote | Pallets Abarrote | - |

#### F. Checklist de Verificación

**Checkboxes (marcar lo que aplica):**
- ☑️ Carga Congelada
- ☑️ Carga Refrigerada
- ☑️ Carga Abarrote
- ☑️ Implementos Completos
- ☑️ Aseo Verificado
- ☑️ Trazabilidad OK
- ☑️ Plataforma WTCK Revisada
- ☑️ Correo WTCK Enviado
- ☑️ Planilla de Despacho Revisada

#### G. Sellos de Seguridad

**Sellos de Salida (5 campos):**
- Sello Salida 1P
- Sello Salida 2P
- Sello Salida 3P
- Sello Salida 4P
- Sello Salida 5P

**Sellos de Retorno (5 campos):**
- Sello Retorno 1P
- Sello Retorno 2P
- Sello Retorno 3P
- Sello Retorno 4P
- Sello Retorno 5P

#### H. Guías de Despacho (21 campos)

```
Guía 1:  [________]    Guía 11: [________]
Guía 2:  [________]    Guía 12: [________]
Guía 3:  [________]    ...
...                    Guía 21: [________]
```

#### I. Certificación y Observaciones

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| N° Certificado Fumigación | Número de certificado | CERT-2026-001 |
| Revisión Limpieza Camión | Observaciones | Aprobado - Sin observaciones |

### 3.3 Comidas Preparadas por Centro de Costo

**Sección Dinámica:**

Cada viaje puede tener comidas preparadas para uno o varios centros de costo.

**Estructura:**

| Elemento | Descripción |
|----------|-------------|
| **[Dropdown Centro de Costo]** | Seleccionar centro existente |
| **[+ Agregar Centro]** | Agregar nuevo centro al viaje |

**Para cada centro de costo, se pueden agregar comidas:**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| Guía Comida | Número de guía | GC-2026-500 |
| Descripción | Descripción del producto | Pollo asado |
| Kilos | Peso en kg | 50.5 |
| Bultos | Cantidad de bultos | 10 |
| Proveedor | Seleccionar proveedor | Proveedor ABC |

**Botones disponibles:**
- **[+ Agregar Centro]**: Añade nuevo centro de costo al viaje
- **[+ Agregar Comida]**: Añade comida al centro actual
- **[+ Nuevo Proveedor]**: Crea proveedor nuevo
- **[Eliminar]**: Elimina comida específica

**Notas:**
- Se pueden agregar múltiples centros de costo por viaje
- Cada centro puede tener múltiples comidas
- Los proveedores se pueden crear sobre la marcha

### 3.4 Guardar el Viaje

**Botones Finales:**
- **[Guardar Viaje]**: Guarda completo
- **[Limpiar Formulario]**: Resetea todos los campos
- **[Cancelar]**: Vuelve al dashboard

**Proceso de Guardado:**
1. Click en "Guardar Viaje"
2. Validación de campos requeridos
3. Confirmación: "¿Guardar viaje V-2026-001?"
4. Guardado en base de datos
5. Actualización de maestras si hay nuevos choferes/casinos
6. Mensaje: "✅ Viaje guardado exitosamente"
7. Redirige a dashboard

---

## 4. EDITAR VIAJE EXISTENTE

### 4.1 Búsqueda de Viajes

**Ruta**: Navegación → Editar Viaje → `/editar-viaje`

**Opciones de Búsqueda:**

1. **Por Número de Viaje**
   - Campo: "Buscar por número de viaje"
   - Ejemplo: V-2026-001
   - Botón "Buscar"

2. **Por Centro de Costo**
   - Dropdown: Centros de costo registrados
   - Filtra viajes por centro

3. **Lista de Viajes Recientes**
   - Tabla con últimos 50 viajes
   - Columnas: Número, Casino, Fecha, Conductor, Acciones

### 4.2 Resultados de Búsqueda

**Tabla de Resultados:**

| N° Viaje | Centro Costo | Casino | Fecha | Conductor | Acciones |
|----------|--------------|--------|-------|-----------|----------|
| V-2026-001 | 12345 | Casino Central | 27/02/2026 | Pedro González | [Editar] [Eliminar] |
| V-2026-002 | 67890 | Casino Norte | 26/02/2026 | María López | [Editar] [Eliminar] |

**Acciones:**
- **[Editar]**: Abre formulario de edición
- **[Eliminar]**: Elimina el viaje (con confirmación)

### 4.3 Formulario de Edición

**Igual que "Nuevo Viaje" pero con datos precargados**

**Diferencias:**
- Botón cambia a **[Actualizar Viaje]**
- Número de viaje no editable
- Comidas preparadas muestran datos existentes
- Botón adicional: **[Eliminar Viaje Completo]**

### 4.4 Actualizar o Eliminar

**Actualizar:**
1. Modificar campos necesarios
2. Click "Actualizar Viaje"
3. Confirmación
4. Guardado
5. Mensaje de éxito

**Eliminar:**
1. Click "Eliminar Viaje Completo"
2. Confirmación: "¿Seguro que desea eliminar V-2026-001 y TODAS sus comidas?"
3. Eliminación en cascada (viaje + comidas)
4. Mensaje: "✅ Viaje eliminado correctamente"
5. Vuelve a lista de viajes

---

## 5. GENERAR PDF

### 5.1 Acceso

**Ruta**: Navegación → Generar PDF → `/generar-pdf`

### 5.2 Selección de Viaje

**Paso 1: Seleccionar Número de Viaje**
- Dropdown con todos los viajes
- Ordenados por más reciente
- Formato: "V-2026-001 - Casino Central"

**Paso 2: Seleccionar Centro de Costo**
- Dropdown con centros asociados al viaje
- Solo aparecen después de seleccionar viaje
-Formato: "12345 - Casino Central"

### 5.3 Opciones de PDF

**Checkboxes:**
- ☑️ Incluir logo DHL
- ☑️ Incluir tabla de comidas
- ☑️ Incluir sellos de seguridad
- ☑️ Dejar espacio para firmas

### 5.4 Generar y Descargar

**Botón**: [Generar PDF]

**Proceso:**
1. Click en "Generar PDF"
2. Mensaje: "Generando PDF..."
3. Servidor crea PDF en carpeta `/pdfs/`
4. Descarga automática comienza
5. Nombre: `Viaje_V-2026-001_12345.pdf`

**Ubicación del archivo:**
- Carpeta `pdfs/` en el servidor
- También descargado en carpeta de descargas del navegador

### 5.5 Estructura del PDF Generado

**El PDF generado incluye las siguientes secciones:**

|Secci\u00f3n | Contenido |
|---------|-----------|
| **Encabezado DHL** | Logo + N\u00famero de viaje |
| **Destino** | Casino, centro de costo, ruta, fecha |
| **Transporte** | Tipo, patente, conductor, RUT, celular |
| **Carga** | Pallets (total y por tipo), wencos, bins |
| **Checklist** | 9 verificaciones marcadas |
| **Comidas** | Tabla con gu\u00eda, descripci\u00f3n, kilos, bultos, proveedor |
| **Sellos** | Salida (5) y Retorno (5) |
| **Gu\u00edas** | 21 gu\u00edas de despacho |
| **Firmas** | Espacios para: Conductor, Bodega DHL, Receptor |

**Ejemplo de contenido:**
- N\u00famero de Viaje: V-2026-001
- Fecha: 27/02/2026  
- Casino: Casino Central (12345)
- Conductor: Pedro Gonz\u00e1lez (RUT: 12.345.678-9)
- Carga: 120 pallets, 50 wencos, 30 bins
- Comidas: M\u00faltiples items con peso, bultos y proveedor

---

## 6. REPORTES EXCEL

### 6.1 Acceso al Panel

**Ruta**: Navegación → Reportes → `/reportes`

### 6.2 Tipos de Reportes Disponibles

#### A. Reporte de Casinos (Maestras)

**Descripción**: Listado completo de centros de costo.

**Columnas:**
- Código de Costo
- Nombre del Casino
- Ruta

**Filtros**: Ninguno

**Botón**: [Descargar Reporte Casinos]

**Nombre archivo**: `reporte_casinos_YYYYMMDD_HHMMSS.xlsx`

#### B. Reporte de Choferes (Maestras)

**Descripción**: Listado completo de conductores.

**Columnas:**
- Nombre Completo
- RUT
- Celular

**Filtros**: Ninguno

**Botón**: [Descargar Reporte Choferes]

**Nombre archivo**: `reporte_choferes_YYYYMMDD_HHMMSS.xlsx`

#### C. Reporte de Comidas e Implementos

**Descripción**: Detalle de todas las comidas preparadas por viaje.

**Columnas:**
- Número de Viaje
- Casino
- Centro de Costo
- Guía Comida
- Descripción
- Kilos
- Bultos
- Proveedor

**Filtros:**
- Fecha Desde
- Fecha Hasta
- Centro de Costo (opcional)

**Botón**: [Descargar Reporte Comidas]

**Nombre archivo**: `reporte_comidas_YYYYMMDD_YYYYMMDD.xlsx`

#### D. Reporte de Viajes Completos

**Descripción**: Información completa de todos los viajes.

**Columnas (más de 60):**
- Número Viaje
- Casino
- Ruta
- Fecha
- Conductor
- RUT
- Celular
- Tipo Camión
- Patentes
- Pallets (todos los tipos)
- Wencos
- Bins
- Checklist completo
- Sellos
- Guías
- Certificaciones

**Filtros:**
- Fecha Desde
- Fecha Hasta
- Centro de Costo (opcional)
- Conductor (opcional)

**Botón**: [Descargar Reporte Viajes Completos]

**Nombre archivo**: `reporte_viajes_completo_YYYYMMDD_YYYYMMDD.xlsx`

#### E. Reporte de Facturación

**Descripción**: Resumen para facturación por centro de costo.

**Columnas:**
- Centro de Costo
- Casino
- Cantidad de Viajes
- Total Pallets
- Total Wencos
- Total Comidas (Kilos)
- Período

**Filtros:**
- Fecha Desde
- Fecha Hasta

**Botón**: [Descargar Reporte Facturación]

**Nombre archivo**: `reporte_facturacion_YYYYMMDD_YYYYMMDD.xlsx`

#### F. Reporte de Control Activos Diario

**Descripción**: Control diario de activos (pallets, wencos).

**Columnas:**
- Fecha
- Número Viaje
- Casino
- Pallets CHEP Salida
- Pallets Negros Salida
- Wencos Salida
- (Similar para Retorno)

**Filtros:**
- Fecha Específica

**Botón**: [Descargar Reporte Activos Diarios]

**Nombre archivo**: `reporte_activos_YYYYMMDD.xlsx`

#### G. Reporte de Rendiciones

**Descripción**: Estado de rendiciones de viajes.

**Columnas:**
- Número Viaje
- PDT
- Ruta
- Fecha Creación
- Estado Rendición
- Fecha Modificación

**Filtros:**
- Estado (SIN REVISAR, APROBADO, RECHAZADO, TODOS)
- Fecha Desde
- Fecha Hasta

**Botón**: [Descargar Reporte Rendiciones]

**Nombre archivo**: `reporte_rendiciones_YYYYMMDD_YYYYMMDD.xlsx`

### 6.3 Proceso de Descarga

**Pasos comunes para todos los reportes:**

1. Seleccionar tipo de reporte
2. Configurar filtros (si aplica)
3. Click en botón "Descargar"
4. Mensaje: "Generando reporte..."
5. Servidor ejecuta query SQL
6. Datos procesados con Pandas
7. Generación de Excel con openpyxl
8. Descarga automática
9. Mensaje: "✅ Reporte generado exitosamente"

**Ubicación de archivos:**
- Descargados en carpeta de Descargas del navegador
- **NO se guardan en el servidor** (generación on-demand)

---

## 7. GESTIÓN DE USUARIOS

### 7.1 Acceso (Solo Administradores)

**Ruta**: Navegación → Usuarios → `/gestionar-usuarios`

**Restricción**: Solo usuarios con rol "admin" pueden acceder.

### 7.2 Lista de Usuarios

**Tabla:**

| ID | Usuario | Nombre Completo | Email | Estado | Acciones |
|----|---------|-----------------|-------|--------|----------|
| 1 | admin | Administrador | admin@dhl.com | Activo | [Cambiar Pass] [Desactivar] |
| 2 | operador1 | Juan Pérez | juan@dhl.com | Activo | [Cambiar Pass] [Desactivar] [Eliminar] |

**Columnas:**
- **ID**: Identificador único
- **Usuario**: Username de login
- **Nombre Completo**: Nombre real
- **Email**: Correo electrónico (opcional)
- **Estado**: Activo / Inactivo
- **Acciones**: Botones de gestión

### 7.3 Crear Nuevo Usuario

**Botón**: [+ Crear Nuevo Usuario]

**Formulario:**

| Campo | Descripción | Requerido | Ejemplo |
|-------|-------------|-----------|---------|
| Username | Nombre de usuario para login | ✅ Sí | operador2 |
| Password | Contraseña | ✅ Sí | [password] |
| Confirmar Password | Repetir contraseña | ✅ Sí | [password] |
| Nombre Completo | Nombre real | ✅ Sí | María López |
| Email | Correo electrónico | ❌ No | maria@dhl.com |

**Validaciones:**
- Username único
- Password mínimo 6 caracteres
- Passwords coinciden

**Botones:**
- **[Crear Usuario]**: Guarda el nuevo usuario
- **[Cancelar]**: Cierra el formulario

### 7.4 Cambiar Contraseña

**Botón**: [Cambiar Pass] en la fila del usuario

**Formulario:**

| Campo | Descripción |
|-------|-------------|
| Nueva Contraseña | Nueva password |
| Confirmar Contraseña | Repetir password |

**Botones:**
- **[Cambiar]**: Actualiza la contraseña
- **[Cancelar]**: Cierra el formulario

### 7.5 Activar/Desactivar Usuario

**Botón**: [Desactivar] o [Activar]

**Efecto:**
- Usuario desactivado NO puede hacer login
- Datos del usuario se conservan
- Reversible (se puede reactivar)

**Nota**: El usuario "admin" no se puede desactivar.

### 7.6 Eliminar Usuario

**Botón**: [Eliminar]

**Confirmación**: "¿Seguro que desea eliminar el usuario 'operador2'?"

**Efecto:**
- Usuario eliminado permanentemente
- NO reversible
- Login asociado ya no funciona

**Nota**: El usuario "admin" no se puede eliminar.

---

## 8. MAESTRAS (Gestión de Datos Maestros)

### 8.1 Gestión de Proveedores

**Acceso**: Reportes → Sección "Proveedores"

**Lista de Proveedores:**

| ID | Nombre Proveedor | Acciones |
|----|------------------|----------|
| 1 | Proveedor ABC | [Editar] [Eliminar] |
| 2 | Proveedor XYZ | [Editar] [Eliminar] |

**Botón**: [+ Agregar Proveedor]

**Formulario:**
- Nombre Proveedor: [______]
- [Guardar] [Cancelar]

### 8.2 Gestión de Transportes

**Acceso**: Reportes → Sección "Transportes"

**Lista de Transportes:**

| Patente | Tipo | Empresa | Acciones |
|---------|------|---------|----------|
| ABCD12 | Refrigerado | Transportes ABC | [Editar] [Eliminar] |

**Botón**: [+ Agregar Transporte]

**Formulario:**
- Patente: [______]
- Tipo: [Dropdown]
- Empresa: [______]
- [Guardar] [Cancelar]

### 8.3 Gestión de Centros de Costo

**Acceso**: Reportes → Sección "Centros de Costo"

**Botón**: [+ Crear Centro de Costo]

**Formulario:**
- Código de Costo: [______]
- Nombre Casino: [______]
- Ruta: [______]
- [Crear] [Cancelar]

### 8.4 Gestión de Choferes

**Acceso**: Reportes → Sección "Choferes"

**Botón**: [+ Crear Chofer]

**Formulario:**
- Nombre Completo: [______]
- RUT: [______]
- Celular: [______]
- [Crear] [Cancelar]

### 8.5 Gestión de Administrativos

**Acceso**: Reportes → Sección "Administrativos"

**Botón**: [+ Crear Administrativo]

**Formulario:**
- Nombre Completo: [______]
- [Crear] [Cancelar]

---

## 9. CARACTERÍSTICAS ESPECIALES

### 9.1 Autocompletado Inteligente

**Campos con autocompletado:**
- Conductor (busca en `maestras_choferes`)
- Centro de Costo (busca en `maestras_casinos`)
- Administrativo (busca en `maestras_administrativos`)
- Proveedor (busca en `proveedores`)

**Funcionamiento:**
1. Escribir al menos 2 caracteres
2. Aparece dropdown con sugerencias
3. Navegar con ↑↓
4. Seleccionar con Enter o Click
5. Datos relacionados se llenan automáticamente

### 9.2 Validación en Tiempo Real

**Validaciones automáticas:**
- Campos requeridos: Borde rojo si vacío
- Formato RUT: Validación de dígito verificador
- Formato fecha: DD/MM/YYYY
- Números: Solo permite dígitos
- Email: Formato válido

**Mensajes de error:**
- Aparecen debajo del campo
- Color rojo
- Desaparecen al corregir

### 9.3 Guardado Automático (Drafts)

**NO implementado actualmente**

**Futuro**: Guardar borradores automáticos cada 30 segundos.

### 9.4 Búsqueda Avanzada

**En Editar Viaje:**
- Búsqueda por número exacto
- Búsqueda por centro de costo
- Filtrado por fecha (futuro)
- Filtrado por conductor (futuro)

### 9.5 Responsive Design

**Adaptación a dispositivos:**
- **Desktop (>1200px)**: Vista completa, 2-3 columnas
- **Tablet (768-1199px)**: Vista media, 2 columnas
- **Mobile (<768px)**: Vista móvil, 1 columna, menú hamburguesa

**Recomendación**: Usar en desktop para mejor experiencia.

---

## 10. SOLUCIÓN DE PROBLEMAS

### 10.1 "No se puede acceder al servidor"

**Síntomas**: Página no carga, timeout.

**Causas y Soluciones:**
1. **Servidor no iniciado**
   - Abrir `SERVIDOR.bat`
   - Click "Iniciar Servidor"

2. **URL incorrecta**
   - Verificar: `http://localhost:5000` (no https)
   - Desde red: usar IP correcta

3. **Firewall bloqueando**
   - Permitir puerto 5000 en Firewall de Windows

### 10.2 "No puedo hacer login"

**Causas:**
1. **Credenciales incorrectas**
   - Verificar usuario: `admin`
   - Verificar password: `admin123` (default)

2. **Usuario desactivado**
   - Contactar administrador para reactivar

3. **Base de datos corrupta**
   - Restaurar desde backup en `_backups_bd/`

### 10.3 "Formulario no guarda"

**Síntomas**: Click en "Guardar" no hace nada.

**Causas:**
1. **Campos requeridos vacíos**
   - Revisar campos con borde rojo
   - Completar todos los requeridos

2. **Error de validación**
   - Ver mensaje de error debajo del campo
   - Corregir formato (RUT, fecha, etc.)

3. **Timeout de sesión**
   - Hacer login nuevamente
   - Volver a intentar guardar

### 10.4 "PDF no se genera"

**Causas:**
1. **Viaje no tiene comidas**
   - Agregar al menos una comida al centro de costo

2. **Centro de costo no seleccionado**
   - Seleccionar centro antes de generar

3. **Error en servidor**
   - Ver log en consola del servidor
   - Contactar soporte técnico

### 10.5 "Reporte Excel vacío"

**Causas:**
1. **Filtros muy restrictivos**
   - Ampliar rango de fechas
   - Quitar filtros opcionales

2. **No hay datos en el período**
   - Verificar que existan viajes en las fechas

---

## 12. BUENAS PRÁCTICAS

### 12.1 Registro de Viajes

✅ **Hacer:**
- Registrar viajes inmediatamente después de completarlos
- Verificar datos antes de guardar
- Usar autocompletado para evitar duplicados
- Agregar todas las comidas con detalles completos

❌ **Evitar:**
- Dejar viajes sin registrar por días
- Guardar con campos requeridos vacíos
- Crear duplicados de choferes/casinos
- Omitir información de comidas

### 12.2 Edición de Viajes

✅ **Hacer:**
- Corregir errores apenas se detecten
- Dejar nota descriptiva si se modifican datos post-viaje
- Verificar que comidas no se pierdan al editar

❌ **Evitar:**
- Editar viajes de meses anteriores sin justificación
- Cambiar número de viaje (mejor eliminar y recrear)
- Eliminar comidas sin verificar

### 12.3 Generación de Reportes

✅ **Hacer:**
- Generar reportes al final del mes
- Guardar reportes con nombre descriptivo
- Verificar que incluyan todos los viajes del período

❌ **Evitar:**
- Generar reportes con rangos de años (muy lentos)
- Confiar en reportes sin verificar datos

### 12.4 Gestión de Maestras

✅ **Hacer:**
- Mantener maestras actualizadas
- Eliminar choferes/casinos que ya no se usan
- Verificar duplicados periódicamente

❌ **Evitar:**
- Crear duplicados con pequeñas variaciones de nombre
- Dejar maestras con datos incompletos

---

## 13. GLOSARIO DE TÉRMINOS

| Término | Definición |
|---------|------------|
| **Viaje** | Registro completo de un transporte de mercadería |
| **Centro de Costo** | Código numérico que identifica un destino/casino |
| **Casino** | Lugar de destino de la carga (comedor, centro de distribución) |
| **Maestra** | Tabla catálogo con datos reutilizables (choferes, casinos, etc.) |
| **Comida Preparada** | Alimento transportado en el viaje, con guía, kilos, bultos |
| **Rendición** | Documento de cierre administrativo del viaje |
| **PDT** | Planilla de Transporte |
| **Wenco** | Contenedor/batea para transporte |
| **Bin** | Contenedor plástico |
| **Pallet** | Tarima/estiba para carga |
| **CHEP** | Marca de pallets azules estandarizados |
| **Guía de Despacho** | Documento que acompaña la carga |
| **Sello** | Sello de seguridad numerado |

---

## 14. CONTACTO Y SOPORTE

### Soporte Técnico

**Problemas con el sistema:**
- Revisar documentación en `_documentacion/`
- Ver logs del servidor en consola de GUI
- Ejecutar `RECREAR_ENTORNO.bat` si hay errores de dependencias

**Recuperación de datos:**
- Backups automáticos en `_backups_bd/`
- Restaurar: Copiar backup sobre `viajes.db` con servidor detenido

**Reportar bugs:**
- Documentar: pasos para reproducir error
- Incluir: captura de pantalla + log del servidor
- Contactar: equipo de desarrollo

---

*Documento generado automáticamente el 27 de Febrero de 2026*
