# 🚀 Cómo Usar el Sistema

## Inicio Rápido

### Opción 1: Interfaz Gráfica (RECOMENDADO)
Ejecuta: **`SERVIDOR.bat`**

Esto abrirá una ventana gráfica donde puedes:
- ▶️ **Iniciar** el servidor
- ⬛ **Detener** el servidor
- 📊 Ver el **log en tiempo real**
- 🔗 Ver las **URLs** de acceso
- 🧹 **Limpiar** procesos Python si hay problemas

### Opción 2: Línea de Comandos
Si prefieres la consola tradicional:
- **Producción**: `iniciar_web.bat`
- **Desarrollo**: `iniciar_desarrollo.bat`

---

## Archivos Disponibles

### ⭐ Uso Diario
- **`SERVIDOR.bat`** - Interfaz gráfica principal
- **`iniciar_web.bat`** - Modo producción (consola)
- **`iniciar_desarrollo.bat`** - Modo desarrollo (consola)

### 🔧 Mantenimiento
- **`RECREAR_ENTORNO.bat`** - Reinstala todo el entorno virtual si hay problemas
- **`reparar_rutas.bat`** - Repara configuraciones de rutas
- **`build_ejecutable.bat`** - Construye versión ejecutable

---

## Solución de Problemas

### El servidor no inicia
1. Ejecuta `RECREAR_ENTORNO.bat` para reinstalar dependencias
2. Usa el botón "🧹 Limpiar Procesos" en la GUI
3. Verifica que el puerto 5000 esté libre

### Error de Python o dependencias faltantes
1. Ejecuta `RECREAR_ENTORNO.bat`
2. Espera 2-3 minutos mientras se reinstala todo
3. Intenta iniciar nuevamente con `SERVIDOR.bat`

### El sistema está lento
1. Abre `SERVIDOR.bat`
2. Usa el botón "🧹 Limpiar Procesos"
3. Esto eliminará procesos Python huérfanos

---

## Acceso al Sistema

Una vez iniciado el servidor, accede desde:
- **Equipo local**: http://localhost:5000
- **Red local**: http://[TU_IP]:5000

Las URLs se muestran en:
- La **ventana de la GUI** (arriba del log)
- La **consola** (si usas .bat tradicional)

---

## Notas Importantes

✅ **Entorno Virtual**: Siempre usa `.venv` - ya está configurado
✅ **Waitress**: Servidor de producción instalado y configurado
✅ **Base de Datos**: `viajes.db` en modo producción
✅ **Puerto**: 5000 (configurable en config.py)

---

*Última actualización: 27 de Febrero de 2026*
