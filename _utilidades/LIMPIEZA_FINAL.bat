@echo off
echo.
echo ========================================
echo  LIMPIEZA FINAL DE SCRIPTS .BAT
echo ========================================
echo.

cd /d "%~dp0"

if not exist "_utilidades" mkdir _utilidades

echo Analizando scripts .bat...
echo.

REM Scripts temporales que ya cumplieron su función
echo [1/3] Eliminando scripts de limpieza temporales...
if exist "LIMPIAR_COMPLETO.bat" (
    del "LIMPIAR_COMPLETO.bat"
    echo   ✓ LIMPIAR_COMPLETO.bat eliminado
)
if exist "LIMPIAR_DIRECTORIO.bat" (
    del "LIMPIAR_DIRECTORIO.bat"
    echo   ✓ LIMPIAR_DIRECTORIO.bat eliminado
)

REM Scripts redundantes - mover a utilidades
echo.
echo [2/3] Moviendo scripts redundantes a _utilidades...
if exist "reparar_entorno.bat" (
    move /Y "reparar_entorno.bat" "_utilidades\"
    echo   ✓ reparar_entorno.bat → _utilidades\
)
if exist "instalar_portable.bat" (
    move /Y "instalar_portable.bat" "_utilidades\"
    echo   ✓ instalar_portable.bat → _utilidades\
)

REM Mover este mismo script a utilidades al final
echo.
echo [3/3] Auto-limpieza...
echo   ℹ Este script se movera a _utilidades al cerrar

echo.
echo ========================================
echo  LIMPIEZA FINAL COMPLETADA
echo ========================================
echo.
echo SCRIPTS .BAT FINALES EN RAÍZ:
echo   ✅ PANEL_CONTROL.bat      (Panel gráfico principal)
echo   ✅ iniciar_web.bat        (Modo producción)
echo   ✅ iniciar_desarrollo.bat (Modo desarrollo)
echo   ✅ reparar_rutas.bat      (Mantenimiento de rutas)
echo   ✅ build_ejecutable.bat   (Crear ejecutable)
echo.
echo Scripts movidos a _utilidades:
echo   📦 reparar_entorno.bat
echo   📦 instalar_portable.bat
echo.
echo TIP: Usa PANEL_CONTROL.bat para gestionar todo!
echo.
pause

REM Auto-mover este script
move /Y "%~f0" "_utilidades\" 2>nul
