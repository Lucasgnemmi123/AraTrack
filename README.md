# # Sistema de Viajes DHL
=========================================

## 🚀 INICIO RÁPIDO

### ▶️ OPCIÓN 1: Panel de Control (RECOMENDADO)
```
Doble click en: PANEL_CONTROL.bat
```
- Interfaz gráfica intuitiva
- Encender/Apagar servidor
- Ver estado en tiempo real
- Acceso rápido a todas las funciones

### ▶️ OPCIÓN 2: Línea de comandos
```
iniciar_web.bat          → Modo producción
iniciar_desarrollo.bat   → Modo desarrollo (con depuración)
```

## 🔐 ACCESO
```
URL:        http://localhost:5000
Usuario:    admin
Contraseña: admin123
```

## 🌐 ACCESO DESDE RED
El servidor acepta conexiones desde otras PCs.
Cuando inicies el servidor verás tu IP local (ej: 192.168.1.100)

Desde otras PCs: `http://IP-DEL-SERVIDOR:5000`

## 📁 ARCHIVOS PRINCIPALES

```
PANEL_CONTROL.bat        ← Panel gráfico (RECOMENDADO)
iniciar_web.bat          ← Modo producción
iniciar_desarrollo.bat   ← Modo desarrollo
reparar_rutas.bat        ← Si hay problemas de rutas
GUIA_USO.txt             ← Guía completa

_scripts_antiguos/       ← Scripts bat antiguos
_utilidades/             ← Scripts de diagnóstico
_logs/                   ← Archivos de log
```

## Sistema de Viajes DHL

Sistema web para gestión de viajes, choferes, centros de costo y generación de PDFs.

## 🚀 Uso Inmediato - TODO INCLUIDO

Esta carpeta contiene **TODO lo necesario** para ejecutar el sistema. No requiere instalación.

### Instrucciones (1 paso):

1. **Doble clic en:**
   ```
   iniciar_web.bat
   ```

2. **Abrir el navegador en:**
   ```
   http://localhost:5000
   ```

¡Eso es todo! El sistema está listo para usar.

## 📋 ¿Qué incluye esta carpeta?

- ✅ Python y todas las librerías necesarias (carpeta `.venv`)
- ✅ Servidor web de producción (Waitress)
- ✅ Base de datos SQLite lista
- ✅ Todas las dependencias instaladas

**Tamaño total:** ~350 MB (incluye entorno Python completo)

## 🔧 Características

- ✅ Interfaz moderna con Bootstrap 5
- ✅ Diseño responsivo y profesional
- ✅ Soporte para múltiples usuarios simultáneos (hasta 10)
- ✅ Gestión de viajes completos
- ✅ Tablas maestras (Choferes, Centros de Costo, Administrativos)
- ✅ Generación automática de PDFs
- ✅ Base de datos optimizada (WAL mode)
- ✅ Funciona sin internet

## 🌐 Acceso en Red Local

Otros usuarios en tu red pueden acceder desde:
```
http://[IP-DE-ESTA-PC]:5000
```

La IP se mostrará al iniciar el sistema.

## 📝 Para Copiar a Otra Computadora

Simplemente copia **toda la carpeta** a la otra computadora y ejecuta `iniciar_web.bat`.

**Importante:** 
- Copia la carpeta completa (incluyendo `.venv`)
- NO requiere instalar Python ni ninguna dependencia
- Funciona directamente

## 🆘 Solución de Problemas

### El navegador no abre la página
- Espera unos segundos a que el servidor inicie
- Intenta con: `http://127.0.0.1:5000`

### "Error al iniciar"
- Verifica que el puerto 5000 no esté ocupado
- Cierra otros programas que puedan usar ese puerto

### Falla al iniciar el .venv
- Asegúrate de copiar TODA la carpeta
- Verifica que la carpeta `.venv` esté completa

## 📞 Notas

- La base de datos se actualiza automáticamente
- Los PDFs se guardan en la carpeta `pdfs/`
- El sistema funciona completamente offline
- Soporta 10 usuarios trabajando al mismo tiempo

---

**Desarrollado para DHL Supply Chain Chile**
