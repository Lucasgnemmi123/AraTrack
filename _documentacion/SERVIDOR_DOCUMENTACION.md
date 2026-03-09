# Documentación del Servidor Web

## Sistema de Viajes DHL - Servidor Waitress + Flask

### Fecha: 27 de Febrero de 2026

---

## 1. ARQUITECTURA DEL SERVIDOR

### Stack de Servidor

```
Cliente (Navegador)
    ↓ HTTP Request
[Puerto 5000]
    ↓
Waitress WSGI Server (Producción)
  • 4 threads concurrentes
  • 0.0.0.0:5000 (todas las interfaces)
  • Timeout: 30s
    ↓
Flask Application (WSGI App)
  • Router de URLs
  • Session Management
  • Template Rendering
    ↓
Business Logic
  • db_manager
  • maestras_manager
  • pdf_generator
  • auth_manager
    ↓
SQLite Database (WAL mode)
  • viajes.db (producción)
  • viajes_dev.db (desarrollo)
```

---

## 2. WAITRESS - SERVIDOR WSGI DE PRODUCCIÓN

### 2.1 ¿Qué es Waitress?

**Waitress** es un servidor WSGI puro Python, diseñado para:
- Producción en entornos Windows/Linux
- Multi-threading para peticiones concurrentes
- Sin dependencias externas (no requiere Apache, nginx)
- Estabilidad y rendimiento adecuado para aplicaciones medianas

### 2.2 Configuración Actual

```python
# En app_web.py (línea 2157+)
from waitress import serve

serve(
    app,                    # Aplicación Flask
    host='0.0.0.0',        # Todas las interfaces de red
    port=5000,             # Puerto HTTP
    threads=4,             # 4 peticiones simultáneas
    channel_timeout=60,    # Timeout de canal
    connection_limit=100   # Límite de conexiones
)
```

**Parámetros Clave:**
- `host='0.0.0.0'` - Escucha en todas las interfaces (localhost + IP de red)
- `port=5000` - Puerto HTTP estándar para desarrollo/interno
- `threads=4` - Hasta 4 peticiones procesadas simultáneamente
- `channel_timeout=60` - Timeout de 60 segundos para requests lentos
- `connection_limit=100` - Máximo 100 conexiones TCP abiertas

### 2.3 Ventajas de Waitress

✅ **Sin dependencias C**: Puro Python, portable  
✅ **Multi-plataforma**: Windows, Linux, macOS  
✅ **Producción-ready**: Usado en empresas con Flask/Pyramid  
✅ **Fácil configuración**: Sin archivos de configuración complejos  
✅ **Gestión automática de threads**: Pool de workers  

### 2.4 Limitaciones

⚠️ **No es nginx**: Sin proxy reverso avanzado  
⚠️ **Sin SSL nativo**: HTTPS requiere proxy frontal  
⚠️ **Escalabilidad media**: ~100 usuarios concurrentes recomendado  
⚠️ **Sin load balancing**: Una sola instancia  

---

## 3. FLASK - FRAMEWORK WEB

### 3.1 Configuración de Flask

```python
app = Flask(__name__)
app.secret_key = 'tu-clave-secreta-aqui'  # Para sesiones
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
```

**Características Activadas:**
- **Sesiones cifradas**: Almacenadas en servidor, cookie solo tiene ID
- **Templates Jinja2**: Renderizado dinámico HTML
- **CSRF protection**: En formularios POST (manual)
- **File uploads**: Desactivados actualmente

### 3.2 Modo Desarrollo vs Producción

| Característica | Desarrollo | Producción |
|---------------|------------|------------|
| Servidor | Flask dev server | Waitress |
| Debug | `debug=True` | `debug=False` |
| Auto-reload | Sí | No |
| Base de datos | `viajes_dev.db` | `viajes.db` |
| Threads | 1 | 4 |
| Host | `127.0.0.1` | `0.0.0.0` |

**Switching entre modos:**
```bash
# Desarrollo
set ARATRACK_ENV=development
python app_web.py

# Producción
set ARATRACK_ENV=production
python app_web.py
```

---

## 4. GESTIÓN DE CONCURRENCIA

### 4.1 Threads de Waitress

Waitress usa un **pool de 4 threads** para manejar peticiones:

```
Request 1 → Thread 1 → Procesando...
Request 2 → Thread 2 → Procesando...
Request 3 → Thread 3 → Procesando...
Request 4 → Thread 4 → Procesando...
Request 5 → [COLA] esperando thread libre...
```

**Timeout por request**: 60 segundos  
**Si se excede**: Request abortado con error 503

### 4.2 Concurrencia en SQLite

SQLite en modo **WAL (Write-Ahead Logging)**:

```
LECTURAS: Ilimitadas simultáneas ✅
ESCRITURAS: 1 a la vez (cola de espera) ⏳
```

**Configuración WAL:**
```python
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('PRAGMA busy_timeout=30000')  # 30 segundos
```

**Comportamiento:**
- Múltiples usuarios pueden **leer** sin bloquearse
- Las **escrituras** se encolan automáticamente
- Si escritura tarda >30s → Error de timeout

### 4.3 Límites de Usuarios Concurrentes

| Escenario | Usuarios Concurrentes | Comportamiento |
|-----------|----------------------|----------------|
| Solo lectura (dashboard, reportes) | ~100+ | Sin problemas |
| Mezcla lectura/escritura | ~50 | Ocasionales esperas |
| Escritura intensiva (creación viajes) | ~10-20 | Colas de espera frecuentes |

**Recomendación**: Máximo 50 usuarios activos simultáneos.

---

## 5. OPTIMIZACIONES DE RENDIMIENTO

### 5.1 Base de Datos

```sql
-- Enabled en config
PRAGMA journal_mode=WAL;        -- Concurrencia de lecturas
PRAGMA synchronous=NORMAL;      -- Balance seguridad/velocidad
PRAGMA cache_size=10000;        -- 10MB de caché
PRAGMA temp_store=MEMORY;       -- Temp tables en RAM
PRAGMA busy_timeout=30000;      -- Timeout de 30s
```

### 5.2 Conexiones de BD

**Patrón por Request:**
```python
def operacion():
    conn = db_manager.get_connection()  # Nueva conexión
    cursor = conn.cursor()
    cursor.execute(...)
    conn.commit()
    conn.close()  # ← CRÍTICO: Cerrar siempre
```

**No usar conexiones globales**: Evita deadlocks en multi-threading.

### 5.3 Timeouts Configurados

| Componente | Timeout | Motivo |
|-----------|---------|--------|
| Waitress channel | 60s | Requests lentos (generación PDF) |
| SQLite busy | 30s | Escrituras en cola |
| Flask session | 8 horas | Sesión de usuario |
| Connection socket | 30s | Red lenta o caída |

---

## 6. INICIO Y DETENCIÓN DEL SERVIDOR

### 6.1 Inicio Manual (Consola)

```bash
# Producción
cd "C:\...\Sistema-Viajes-DHL"
.venv\Scripts\activate
set ARATRACK_ENV=production
python app_web.py
```

**Salida esperada:**
```
============================================================
Sistema de Viajes DHL - PRODUCCIÓN
============================================================
Entorno: production
Base de datos: viajes.db
Puerto: 5000

Acceso LOCAL (esta PC):
   http://localhost:5000
   http://127.0.0.1:5000

Acceso RED LOCAL (otras PCs en la red):
   http://192.168.1.100:5000

Usuarios simultáneos: 4
Servidor: Waitress (producción)
============================================================
```

### 6.2 Inicio con GUI

```bash
# Doble clic en:
SERVIDOR.bat

# O desde PowerShell:
.\SERVIDOR.bat
```

**La GUI permite:**
- ▶️ Iniciar servidor con un clic
- ⬛ Detener servidor con un clic
- 📋 Ver log en tiempo real (colores)
- 🧹 Limpiar procesos Python huérfanos
- 🔍 Ver estado (Ejecutando / Detenido)
- 🔗 Ver URLs de acceso

### 6.3 Detención Segura

**Desde GUI**: Botón "⬛ DETENER SERVIDOR"  
**Desde consola**: `Ctrl+C` → Flask captura señal y cierra limpiamente

**Proceso de shutdown:**
1. Waitress deja de aceptar nuevas conexiones
2. Espera a que terminen requests en curso (max 60s)
3. Cierra conexiones SQLite pendientes
4. Termina proceso Python

---

## 7. ACCESO AL SERVIDOR

### 7.1 URLs de Acceso

**Localhost (misma PC):**
- `http://localhost:5000`
- `http://127.0.0.1:5000`

**Red Local (otras PCs en la LAN):**
- `http://[IP-DEL-SERVIDOR]:5000`
- Ejemplo: `http://192.168.1.100:5000`

**IP Dinámica**: Se muestra automáticamente al iniciar servidor.

### 7.2 Requisitos de Red

✅ **Puerto 5000 abierto** en firewall de Windows  
✅ **Red privada o de trabajo** (no pública)  
✅ **PCs en la misma subred** (mismo rango IP)  

**Verificar acceso remoto:**
```powershell
# Desde otra PC:
Test-NetConnection -ComputerName 192.168.1.100 -Port 5000
```

### 7.3 Firewall de Windows

**Abrir puerto 5000:**
```powershell
# Como administrador:
netsh advfirewall firewall add rule name="AraTrack Server" dir=in action=allow protocol=TCP localport=5000
```

---

## 8. MONITOREO Y DIAGNÓSTICO

### 8.1 Verificar Puerto Ocupado

```powershell
# Verificar si puerto 5000 está en uso:
netstat -ano | findstr :5000

# Ver proceso usando el puerto:
tasklist /FI "PID eq [PID_NÚMERO]"
```

### 8.2 Ver Procesos Python Activos

```powershell
Get-Process python* | Select-Object Id, ProcessName, StartTime, CPU
```

### 8.3 Logs de Errores

**Consola del servidor**: Todos los logs van a stdout/stderr  
**Captura en GUI**: Log area muestra todo en tiempo real  
**Archivo de log**: `_logs/diagnostico.txt` (si está habilitado)

**Tipos de log:**
- `[OK]` - Operación exitosa (verde en GUI)
- `[!]` - Advertencia (amarillo en GUI)
- `ERROR` - Error crítico (rojo en GUI)

---

## 9. SOLUCIÓN DE PROBLEMAS COMUNES

### 9.1 "Puerto 5000 ya está en uso"

**Causa**: Otro proceso (Python, NodeJS, etc.) usando el puerto.

**Solución:**
```powershell
# Identificar proceso:
netstat -ano | findstr :5000

# Matar proceso (reemplaza [PID] con el número):
taskkill /F /PID [PID]

# O usar GUI: Botón "Limpiar Procesos"
```

### 9.2 "Waitress no encontrado"

**Causa**: Entorno virtual sin Waitress instalado.

**Solución:**
```bash
# Recrear entorno virtual:
.\RECREAR_ENTORNO.bat

# O instalar manualmente:
.venv\Scripts\pip install waitress==3.0.2
```

### 9.3 "Database is locked"

**Causa**: Dos escrituras simultáneas o conexión no cerrada.

**Solución:**
```python
# Siempre cerrar conexiones:
conn = db_manager.get_connection()
try:
    # ... operaciones ...
finally:
    conn.close()  # ← CRÍTICO
```

### 9.4 Servidor no responde

**Síntomas**: Requests cuelgan, timeouts.

**Causas posibles:**
1. Deadlock en SQLite
2. Query infinito/bloqueado
3. Thread pool saturado

**Solución:**
```bash
# Reiniciar servidor:
1. Detener (Ctrl+C o GUI)
2. Esperar 5 segundos
3. Limpiar procesos (GUI o taskkill)
4. Iniciar nuevamente
```

### 9.5 Acceso desde red no funciona

**Verificar:**
1. ✅ Servidor escuchando en `0.0.0.0` (no `127.0.0.1`)
2. ✅ Firewall Windows permite puerto 5000
3. ✅ Red configurada como "Privada" (no "Pública")
4. ✅ Ambas PCs en la misma subred

---

## 10. MEJORAS FUTURAS

### 10.1 Escalabilidad

Para más de 100 usuarios:
- **PostgreSQL** en lugar de SQLite
- **Gunicorn** con múltiples workers (Linux)
- **nginx** como proxy reverso
- **Redis** para caché de sesiones

### 10.2 Seguridad

- **HTTPS**: Certificado SSL (Let's Encrypt)
- **Nginx proxy**: Terminación SSL, rate limiting
- **Autenticación OAuth**: Login con Microsoft/Google
- **Audit log**: Registro de todas las operaciones

### 10.3 Alta Disponibilidad

- **Load balancer**: Múltiples instancias de Waitress
- **Replicación BD**: Master-Slave PostgreSQL
- **Health checks**: Monitoreo automático
- **Auto-restart**: Supervisor o systemd

---

## 11. COMPARACIÓN DE SERVIDORES

| Característica | Flask Dev | Waitress | Gunicorn | nginx+uWSGI |
|---------------|-----------|----------|----------|-------------|
| Plataforma | Cualquiera | Cualquiera | Linux/Mac | Linux |
| Threads | 1 | Configurable | Configurable | Configurable |
| Producción | ❌ | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ❌ | ❌ |
| Setup | Trivial | Fácil | Medio | Complejo |
| Performance | Bajo | Medio | Alto | Muy Alto |
| SSL | ❌ | ❌ | ❌ | ✅ |

**Veredicto**: Waitress es ideal para producción en Windows, red interna, <100 usuarios.

---

## 12. REFERENCIAS

### Documentación Oficial
- **Waitress**: https://docs.pylonsproject.org/projects/waitress/
- **Flask**: https://flask.palletsprojects.com/
- **SQLite WAL**: https://www.sqlite.org/wal.html

### Archivos Relacionados
- `app_web.py` - Configuración de servidor (líneas 2135-2181)
- `config.py` - Variables de configuración
- `servidor_gui.py` - GUI de control
- `ARQUITECTURA_APLICACION.md` - Documentación de la aplicación

---

*Documento generado automáticamente el 27 de Febrero de 2026*
