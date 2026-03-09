@echo off
setlocal enabledelayedexpansion
echo ========================================
echo  Sistema de Viajes DHL
echo  Reparar Rutas del Entorno Virtual
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar que existe .venv
if not exist ".venv" (
    echo ERROR: No se encuentra la carpeta .venv
    echo.
    echo Ejecuta primero: instalar_portable.bat
    echo.
    pause
    exit /b 1
)

echo Ubicacion actual: %CD%
echo.
echo Actualizando rutas en el entorno virtual...
echo.

REM Obtener la ruta actual (escapando backslashes para regex)
set "NUEVA_RUTA=%CD%"

REM Actualizar pyvenv.cfg
if exist ".venv\pyvenv.cfg" (
    echo [1/3] Actualizando pyvenv.cfg...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ruta='%NUEVA_RUTA%'; $file='.venv\pyvenv.cfg'; $content=Get-Content $file -Raw; $content=$content -replace 'home\s*=\s*.*', ('home = ' + $ruta + '\.venv\Scripts'); Set-Content $file $content -NoNewline"
)

REM Actualizar Activate.ps1
if exist ".venv\Scripts\Activate.ps1" (
    echo [2/3] Actualizando Activate.ps1...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ruta='%NUEVA_RUTA%'; $file='.venv\Scripts\Activate.ps1'; $content=Get-Content $file -Raw; $content=$content -replace '\$env:VIRTUAL_ENV\s*=\s*"".*""', ('$env:VIRTUAL_ENV=\"' + $ruta + '\.venv\"'); Set-Content $file $content -NoNewline"
)

REM Actualizar pip para regenerar sus scripts
if exist ".venv\Scripts\python.exe" (
    echo [3/3] Regenerando scripts de pip...
    .venv\Scripts\python.exe -m pip install --upgrade --force-reinstall --no-deps pip setuptools >nul 2>&1
)

echo.
echo ========================================
echo  Rutas Actualizadas!
echo ========================================
echo.
echo El entorno virtual esta listo para usar.
echo Ahora ejecuta: iniciar_web.bat
echo.

pause
