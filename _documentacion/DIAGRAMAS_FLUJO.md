# Diagramas de Flujo del Sistema

## Sistema de Viajes DHL - Flujos de Procesos

### Fecha: 27 de Febrero de 2026

---

## 1. FLUJO GENERAL DEL SISTEMA

```mermaid
graph TB
    A[Usuario accede a http://localhost:5000] --> B{¿Sesión activa?}
    B -->|No| C[Mostrar pantalla Login]
    B -->|Sí| D[Mostrar Dashboard]
    C --> E[Usuario ingresa credenciales]
    E --> F{¿Credenciales válidas?}
    F -->|No| G[Mostrar error]
    G --> C
    F -->|Sí| H[Crear sesión]
    H --> D
    D --> I{Seleccionar acción}
    I -->|Nuevo Viaje| J[Formulario Nuevo Viaje]
    I -->|Editar Viaje| K[Búsqueda de Viajes]
    I -->|Generar PDF| L[Selección de Viaje]
    I -->|Reportes| M[Panel de Reportes]
    I -->|Usuarios| N[Gestión de Usuarios]
    I -->|Logout| O[Cerrar sesión]
    O --> C
```

---

## 2. FLUJO DE CREACIÓN DE VIAJE

```mermaid
flowchart TD
    A[Inicio: Nuevo Viaje] --> B[Cargar formulario]
    B --> C[Llenar Información Básica]
    C --> D[Número de Viaje<br>Fecha<br>Casino<br>Administrativo]
    D --> E[Información del Transporte]
    E --> F[Tipo Camión<br>Patentes<br>Termógrafos]
    F --> G[Información del Conductor]
    G --> H{¿Conductor existe<br>en maestras?}
    H -->|Sí| I[Autocompletar RUT y Celular]
    H -->|No| J[Ingresar manualmente]
    I --> K[Fechas de Operación]
    J --> K
    K --> L[Llegada DHL<br>Salida DHL]
    L --> M[Información de Carga]
    M --> N[Pallets<br>Wencos<br>Bins]
    N --> O[Checklist de Verificación]
    O --> P[Sellos de Seguridad]
    P --> Q[Guías de Despacho]
    Q --> R[Certificación y Observaciones]
    R --> S[Agregar Centros de Costo]
    S --> T{¿Más centros?}
    T -->|Sí| U[+ Agregar Centro]
    U --> V[Por cada centro:<br>Agregar Comidas Preparadas]
    T -->|No| V
    V --> W[Guía<br>Descripción<br>Kilos<br>Bultos<br>Proveedor]
    W --> X{¿Más comidas<br>en este centro?}
    X -->|Sí| V
    X -->|No| Y{¿Validación OK?}
    Y -->|No| Z[Mostrar errores]
    Z --> C
    Y -->|Sí| AA[Click: Guardar Viaje]
    AA --> AB[Confirmar guardado]
    AB --> AC[DB: INSERT INTO viajes]
    AC --> AD[DB: INSERT INTO comidas_preparadas]
    AD --> AE{¿Conductor nuevo?}
    AE -->|Sí| AF[Agregar a maestras_choferes]
    AE -->|No| AG{¿Casino nuevo?}
    AF --> AG
    AG -->|Sí| AH[Agregar a maestras_casinos]
    AG -->|No| AI[Mostrar éxito]
    AH --> AI
    AI --> AJ[Redirigir a Dashboard]
    AJ --> AK[Fin]
```

---

## 3. FLUJO DE EDICIÓN DE VIAJE

```mermaid
flowchart TD
    A[Inicio: Editar Viaje] --> B[Cargar interfaz de búsqueda]
    B --> C{Método de búsqueda}
    C -->|Número| D[Ingresar número de viaje]
    C -->|Centro| E[Seleccionar centro de costo]
    C -->|Lista| F[Ver lista de viajes recientes]
    D --> G[Click: Buscar]
    E --> G
    F --> H[Seleccionar viaje de la lista]
    G --> I{¿Viaje encontrado?}
    H --> I
    I -->|No| J[Mostrar: No se encontraron resultados]
    J --> B
    I -->|Sí| K[Mostrar resultados]
    K --> L{Acción}
    L -->|Editar| M[DB: SELECT viaje completo]
    L -->|Eliminar| N[Confirmar eliminación]
    N --> O[DB: DELETE viaje CASCADE comidas]
    O --> P[Mostrar éxito]
    P --> B
    M --> Q[Cargar formulario precargado]
    Q --> R[Modificar campos necesarios]
    R --> S{¿Validación OK?}
    S -->|No| T[Mostrar errores]
    T --> R
    S -->|Sí| U[Click: Actualizar Viaje]
    U --> V[DB: UPDATE viajes SET ...]
    V --> W[DB: DELETE comidas anteriores]
    W --> X[DB: INSERT nuevas comidas]
    X --> Y[Actualizar maestras si es necesario]
    Y --> Z[Mostrar éxito]
    Z --> AA[Redirigir a Dashboard]
    AA --> AB[Fin]
```

---

## 4. FLUJO DE GENERACIÓN DE PDF

```mermaid
flowchart TD
    A[Inicio: Generar PDF] --> B[Cargar interfaz]
    B --> C[Cargar dropdown con viajes]
    C --> D[Usuario selecciona número de viaje]
    D --> E[DB: SELECT centros de costo del viaje]
    E --> F[Cargar dropdown con centros]
    F --> G[Usuario selecciona centro de costo]
    G --> H[Configurar opciones de PDF]
    H --> I[Incluir logo DHL?<br>Incluir comidas?<br>Incluir sellos?<br>Espacio para firmas?]
    I --> J[Click: Generar PDF]
    J --> K[POST /api/generar-pdf]
    K --> L[DB: SELECT viaje completo WHERE numero_viaje AND centro_costo]
    L --> M[DB: SELECT comidas_preparadas WHERE viaje AND centro]
    M --> N[pdf_generator.generar_pdf]
    N --> O[ReportLab: Crear documento]
    O --> P[Agregar logo DHL]
    P --> Q[Agregar información del viaje]
    Q --> R[Agregar tabla de transporte]
    R --> S[Agregar información de conductor]
    S --> T[Agregar tabla de carga]
    T --> U[Agregar checklist]
    U --> V{¿Incluir comidas?}
    V -->|Sí| W[Agregar tabla comidas preparadas]
    V -->|No| X
    W --> X[Agregar sellos salida/retorno]
    X --> Y[Agregar guías de despacho]
    Y --> Z{¿Espacio firmas?}
    Z -->|Sí| AA[Agregar sección de firmas]
    Z -->|No| AB
    AA --> AB[Guardar PDF en /pdfs/]
    AB --> AC[Generar nombre: Viaje_Nro_Centro.pdf]
    AC --> AD[Retornar URL de descarga]
    AD --> AE[Cliente recibe response]
    AE --> AF[Navegador inicia descarga automática]
    AF --> AG[PDF descargado]
    AG --> AH[Fin]
```

---

## 5. FLUJO DE GENERACIÓN DE REPORTES EXCEL

```mermaid
flowchart TD
    A[Inicio: Reportes] --> B[Cargar panel de reportes]
    B --> C{Seleccionar tipo de reporte}
    C -->|Casinos| D[Reporte Maestras Casinos]
    C -->|Choferes| E[Reporte Maestras Choferes]
    C -->|Comidas| F[Reporte Comidas e Implementos]
    C -->|Viajes| G[Reporte Viajes Completos]
    C -->|Facturación| H[Reporte Facturación]
    C -->|Activos| I[Reporte Control Activos]
    C -->|Rendiciones| J[Reporte Rendiciones]
    
    D --> K[Sin filtros]
    E --> K
    
    F --> L[Configurar filtros]
    G --> L
    H --> L
    I --> L
    J --> L
    
    K --> M[Click: Descargar]
    L --> N[Fecha Desde<br>Fecha Hasta<br>Centro Costo<br>Conductor<br>Estado]
    N --> M
    
    M --> O[POST /api/descargar-reporte-*]
    O --> P[Leer archivo SQL de queries/]
    P --> Q[DB: Ejecutar query con filtros]
    Q --> R[Obtener resultados: List Dict ]
    R --> S[pandas.DataFrame resultados ]
    S --> T[Aplicar filtros adicionales]
    T --> U[Formatear columnas]
    U --> V[Configurar estilos Excel]
    V --> W[df.to_excel engine=openpyxl ]
    W --> X[Generar BytesIO buffer]
    X --> Y[send_file buffer, mimetype=xlsx]
    Y --> Z[Cliente recibe archivo]
    Z --> AA[Navegador descarga Excel]
    AA --> AB[Usuario abre archivo]
    AB --> AC[Fin]
```

---

## 6. FLUJO DE AUTENTICACIÓN

```mermaid
sequenceDiagram
    participant U as Usuario
    participant B as Navegador
    participant F as Flask App
    participant A as AuthManager
    participant D as SQLite DB
    
    U->>B: Accede a http://localhost:5000
    B->>F: GET /
    F->>F: Verificar sesión
    F-->>B: Redirect /login (sin sesión)
    B-->>U: Mostrar formulario login
    
    U->>B: Ingresa username + password
    B->>F: POST /login
    F->>A: verificar_credenciales(username, password)
    A->>D: SELECT * FROM usuarios WHERE username=?
    D-->>A: Usuario encontrado
    A->>A: bcrypt.checkpw(password, hash)
    A-->>F: Credenciales válidas
    F->>F: session['user_id'] = user_id
    F->>F: session['username'] = username
    F-->>B: Redirect /dashboard
    B-->>U: Mostrar dashboard
    
    U->>B: Navega a sección protegida
    B->>F: GET /ruta-protegida
    F->>F: @login_required verifica sesión
    F->>F: session.get('user_id') != None
    F-->>B: Retorna contenido autorizado
    B-->>U: Muestra contenido
```

---

## 7. FLUJO DE GESTIÓN DE MAESTRAS

```mermaid
flowchart TD
    A[Inicio: Gestión Maestras] --> B{Tipo de maestra}
    B -->|Choferes| C[maestras_choferes]
    B -->|Casinos| D[maestras_casinos]
    B -->|Administrativos| E[maestras_administrativos]
    B -->|Proveedores| F[proveedores]
    B -->|Transportes| G[transportes]
    
    C --> H[Listar todos los choferes]
    D --> I[Listar todos los casinos]
    E --> J[Listar todos los administrativos]
    F --> K[Listar todos los proveedores]
    G --> L[Listar todos los transportes]
    
    H --> M{Acción}
    I --> M
    J --> M
    K --> M
    L --> M
    
    M -->|Crear| N[Formulario vacío]
    M -->|Editar| O[Formulario precargado]
    M -->|Eliminar| P[Confirmar eliminación]
    
    N --> Q[Usuario llena campos]
    Q --> R{¿Validación OK?}
    R -->|No| S[Mostrar errores]
    S --> Q
    R -->|Sí| T[DB: INSERT INTO maestra]
    T --> U{¿Ya existe?}
    U -->|Sí| V[Error: Duplicado]
    V --> Q
    U -->|No| W[Inserción exitosa]
    W --> X[Actualizar lista]
    
    O --> Y[Usuario modifica campos]
    Y --> Z{¿Validación OK?}
    Z -->|No| AA[Mostrar errores]
    AA --> Y
    Z -->|Sí| AB[DB: UPDATE maestra SET ... WHERE id=?]
    AB --> AC[Actualización exitosa]
    AC --> X
    
    P --> AD{¿Confirmar?}
    AD -->|No| X
    AD -->|Sí| AE[DB: DELETE FROM maestra WHERE id=?]
    AE --> AF{¿Tiene referencias?}
    AF -->|Sí| AG[Error: No se puede eliminar]
    AF -->|No| AH[Eliminación exitosa]
    AG --> X
    AH --> X
    
    X --> AI[Mostrar lista actualizada]
    AI --> AJ[Fin]
```

---

## 8. FLUJO DE GESTIÓN DE USUARIOS

```mermaid
flowchart TD
    A[Inicio: Gestión Usuarios] --> B{¿Es admin?}
    B -->|No| C[Error: Acceso denegado]
    C --> D[Redirect Dashboard]
    B -->|Sí| E[Cargar /gestionar-usuarios]
    E --> F[DB: SELECT * FROM usuarios]
    F --> G[Mostrar lista de usuarios]
    G --> H{Acción}
    H -->|Crear| I[Formulario nuevo usuario]
    H -->|Cambiar Pass| J[Formulario cambiar password]
    H -->|Activar/Desactivar| K[Toggle estado]
    H -->|Eliminar| L[Confirmar eliminación]
    
    I --> M[Username<br>Password<br>Confirmar Pass<br>Nombre<br>Email]
    M --> N{¿Validación OK?}
    N -->|No| O[Mostrar errores]
    O --> M
    N -->|Sí| P[bcrypt.hashpw password ]
    P --> Q[DB: INSERT INTO usuarios]
    Q --> R{¿Username único?}
    R -->|No| S[Error: Usuario ya existe]
    S --> M
    R -->|Sí| T[Usuario creado]
    T --> U[Actualizar lista]
    
    J --> V[Nueva password<br>Confirmar password]
    V --> W{¿Validación OK?}
    W -->|No| X[Mostrar errores]
    X --> V
    W -->|Sí| Y[bcrypt.hashpw nueva_pass ]
    Y --> Z[DB: UPDATE usuarios SET password_hash=? WHERE id=?]
    Z --> AA[Password cambiado]
    AA --> U
    
    K --> AB[DB: UPDATE usuarios SET activo=NOT activo WHERE id=?]
    AB --> AC[Estado actualizado]
    AC --> U
    
    L --> AD{¿Confirmar?}
    AD -->|No| U
    AD -->|Sí| AE{¿Es admin primario?}
    AE -->|Sí| AF[Error: No se puede eliminar admin]
    AF --> U
    AE -->|No| AG[DB: DELETE FROM usuarios WHERE id=?]
    AG --> AH[Usuario eliminado]
    AH --> U
    
    U --> AI[Mostrar lista actualizada]
    AI --> AJ[Fin]
```

---

## 9. FLUJO DE INICIO/DETENCIÓN DEL SERVIDOR

```mermaid
flowchart TD
    A[Usuario: Doble click SERVIDOR.bat] --> B[PowerShell ejecuta:]
    B --> C[pythonw.exe servidor_gui.py]
    C --> D[Cargar ventana tkinter]
    D --> E[Verificar puerto 5000]
    E --> F{¿Puerto ocupado?}
    F -->|Sí| G[Mostrar: Servidor ya corriendo]
    F -->|No| H[Mostrar: ⚫ DETENIDO]
    G --> I[Estado: 🟢 EJECUTANDO]
    H --> J{Usuario presiona botón}
    I --> J
    
    J -->|▶ Iniciar| K[Validar .venv/Scripts/python.exe]
    J -->|⬛ Detener| L[proceso_servidor.terminate]
    J -->|🧹 Limpiar| M[Proteger PIDs propios]
    
    K --> N{¿Existe?}
    N -->|No| O[Error: Ejecuta RECREAR_ENTORNO.bat]
    O --> H
    N -->|Sí| P[set ARATRACK_ENV=production]
    P --> Q[subprocess.Popen python app_web.py ]
    Q --> R[Thread: leer stdout/stderr]
    R --> S[app_web.py: from waitress import serve]
    S --> T[serve app, host=0.0.0.0, port=5000, threads=4 ]
    T --> U[Waitress escuchando en 0.0.0.0:5000]
    U --> V[Mostrar en log: URLs de acceso]
    V --> W[Estado: 🟢 EJECUTANDO]
    W --> X[Capturar stdout en tiempo real]
    X --> Y[Mostrar en log con colores]
    Y --> I
    
    L --> Z[proceso.wait timeout=5s ]
    Z --> AA{¿Terminó?}
    AA -->|No| AB[proceso.kill]
    AA -->|Sí| AC[Proceso terminado]
    AB --> AC
    AC --> AD[Log: ✓ Servidor detenido]
    AD --> H
    
    M --> AE[mi_pid = os.getpid]
    AE --> AF[pids_excluir = mi_pid, servidor.pid, padres ]
    AF --> AG[psutil.process_iter]
    AG --> AH[Por cada proceso python:]
    AH --> AI{¿PID en excluir?}
    AI -->|Sí| AJ[Saltar proteger ]
    AI -->|No| AK[proc.kill]
    AJ --> AL{¿Más procesos?}
    AK --> AL
    AL -->|Sí| AH
    AL -->|No| AM[Log: N procesos eliminados]
    AM --> AN[Estado actual mantiene]
    AN --> I
```

---

## 10. FLUJO DE CONCURRENCIA EN SQLite

```mermaid
sequenceDiagram
    participant U1 as Usuario 1
    participant U2 as Usuario 2
    participant U3 as Usuario 3
    participant W as Waitress Thread
    participant DB as SQLite WAL
    
    Note over DB: Modo WAL activado
    
    U1->>W: GET /dashboard (lectura)
    U2->>W: GET /reportes (lectura)
    U3->>W: POST /api/guardar-viaje (escritura)
    
    W->>DB: Thread 1: SELECT viajes
    W->>DB: Thread 2: SELECT comidas
    W->>DB: Thread 3: BEGIN TRANSACTION
    
    par Lecturas simultáneas
        DB-->>W: Thread 1: Resultados
        DB-->>W: Thread 2: Resultados
    end
    
    W-->>U1: Respuesta dashboard
    W-->>U2: Respuesta reportes
    
    W->>DB: Thread 3: INSERT INTO viajes
    DB-->>W: Thread 3: COMMIT OK
    W-->>U3: Viaje guardado
    
    Note over U1,U3: Nuevos requests
    
    U1->>W: POST /api/guardar-viaje (escritura 2)
    U2->>W: POST /api/actualizar-viaje (escritura 3)
    
    W->>DB: Thread 1: BEGIN TRANSACTION
    W->>DB: Thread 2: BEGIN TRANSACTION (espera)
    
    Note over DB: Thread 2 en cola<br/>busy_timeout=30s
    
    W->>DB: Thread 1: INSERT + COMMIT
    DB-->>W: Thread 1: OK
    
    Note over DB: Libera lock
    
    W->>DB: Thread 2: Procesa UPDATE
    DB-->>W: Thread 2: COMMIT OK
    
    W-->>U1: Escritura 2 exitosa
    W-->>U2: Escritura 3 exitosa
```

---

## 11. FLUJO DE MANEJO DE ERRORES

```mermaid
flowchart TD
    A[Request entrante] --> B{Tipo de request}
    B -->|GET| C[try: Ejecutar lógica]
    B -->|POST| D[try: Validar datos]
    
    C --> E{¿Error?}
    D --> F{¿Validación OK?}
    
    F -->|No| G[return jsonify error:message , 400]
    F -->|Sí| H[try: Ejecutar lógica]
    H --> E
    
    E -->|No| I[return render_template / jsonify success]
    E -->|Sí| J{Tipo de error}
    
    J -->|sqlite3.Error| K[Log: Database error]
    J -->|ValueError| L[Log: Validation error]
    J -->|FileNotFoundError| M[Log: File not found]
    J -->|Exception| N[Log: Unexpected error]
    
    K --> O[return jsonify error:DB_error , 500]
    L --> P[return jsonify error:Invalid_data , 400]
    M --> Q[return jsonify error:File_not_found , 404]
    N --> R[return jsonify error:Server_error , 500]
    
    O --> S[Cliente recibe error]
    P --> S
    Q --> S
    R --> S
    
    S --> T[JavaScript: mostrar alerta]
    T --> U[Usuario ve mensaje de error]
    U --> V{¿Puede corregir?}
    V -->|Sí| W[Usuario corrige y reintenta]
    V -->|No| X[Usuario contacta soporte]
    W --> A
    X --> Y[Revisar logs del servidor]
    Y --> Z[Fin]
```

---

## 12. DIAGRAMA DE COMPONENTES

```mermaid
graph TB
    subgraph "Frontend Navegador"
        A[HTML Templates Jinja2]
        B[CSS Styles]
        C[JavaScript AJAX]
        D[jQuery]
    end
    
    subgraph "Flask Application"
        E[app_web.py Router]
        F[auth_manager.py]
        G[db_manager.py]
        H[maestras_manager.py]
        I[pdf_generator.py]
        J[rendiciones_manager.py]
        K[config.py]
    end
    
    subgraph "Servidor WSGI"
        L[Waitress Server]
        M[Thread Pool 4]
    end
    
    subgraph "Base de Datos"
        N[SQLite viajes.db]
        O[WAL Mode]
        P[viajes table]
        Q[comidas_preparadas table]
        R[maestras_* tables]
        S[usuarios table]
    end
    
    subgraph "Archivos Generados"
        T[PDFs]
        U[Reportes Excel]
    end
    
    A --> C
    C --> D
    D --> E
    B --> A
    
    E --> F
    E --> G
    E --> H
    E --> I
    E --> J
    F --> K
    G --> K
    H --> K
    
    E --> L
    L --> M
    M --> E
    
    G --> N
    H --> N
    N --> O
    N --> P
    N --> Q
    N --> R
    N --> S
    
    I --> T
    E --> U
    
    style L fill:#90EE90
    style N fill:#FFB6C1
    style E fill:#87CEEB
```

---

*Documento generado automáticamente el 27 de Febrero de 2026*

**Nota**: Los diagramas Mermaid pueden ser visualizados en:
- GitHub
- VS Code con extensión Mermaid Preview
- Herramientas online: mermaid.live
