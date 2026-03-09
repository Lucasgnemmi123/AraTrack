@echo off
echo ========================================
echo  AraTrack - Modo DESARROLLO
echo ========================================
echo.

cd /d "%~dp0"

REM Establecer entorno de desarrollo
set ARATRACK_ENV=development

REM Activar entorno virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ADVERTENCIA: No se encuentra el entorno virtual
    echo El script continuará sin activar el entorno virtual
    echo.
)

echo Configuracion:
echo   - Entorno: DESARROLLO
echo   - Base de datos: viajes_dev.db
echo   - Puerto: 5001
echo.
echo Iniciando servidor...
echo.

python app_web.py

pause
