# AraTrack - Versión Portable

## Para el Desarrollador (TÚ)

### Generar el Ejecutable Portable:

1. Asegúrate de tener todos los archivos actualizados
2. Ejecuta: `build_ejecutable.bat`
3. Espera a que termine (puede tardar 2-3 minutos)
4. El ejecutable estará en `dist\AraTrack.exe`

### Compartir con Otro Usuario:

**Opción 1 - Solo Ejecutable (Más limpio):**
Crea una carpeta nueva y copia:
- `dist\AraTrack.exe`
- `datos.xlsx` (si lo necesitan)
- `viajes_dhl.db` (si quieres compartir datos existentes)

**Opción 2 - Carpeta Completa:**
Comprime la carpeta `dist\` completa y compártela

---

## Para el Usuario Final (OTRA PERSONA)

### Instalación - CERO PASOS:
✅ NO necesita instalar Python
✅ NO necesita instalar librerías
✅ NO necesita configurar nada

### Uso:

1. **Descomprimir** la carpeta en cualquier lugar
2. **Doble clic** en `AraTrack.exe`
3. **Esperar** 2-3 segundos
4. El navegador se abrirá automáticamente en `http://localhost:5000`
5. **Iniciar sesión** con las credenciales proporcionadas

### Usuarios por Defecto:
- **Admin**: admin / admin123
- **Usuario**: usuario / usuario123

### Importante:
- NO cerrar la ventana negra (consola) mientras uses la app
- Para cerrar la aplicación: Cierra la ventana negra
- Los datos se guardan en `viajes_dhl.db` en la misma carpeta

### Solución de Problemas:

**Si no abre el navegador:**
- Abre manualmente: http://localhost:5000

**Si dice "Puerto ocupado":**
- Cierra otros AraTrack.exe que estén corriendo
- O reinicia el equipo

**Si no funciona:**
- Verifica que no tengas antivirus bloqueando el .exe
- Ejecuta como Administrador (clic derecho → Ejecutar como administrador)

---

## Requisitos del Sistema (Usuario Final)

- Windows 7 o superior
- 100 MB de espacio libre
- Conexión de red NO requerida (funciona offline)
