@echo off
echo ========================================
echo  INICIANDO SISTEMA - Capturando Output
echo ========================================
echo.
cd /d "%~dp0"

REM Establecer modo PRODUCCIÓN
set ARATRACK_ENV=production

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Redirigir todo a archivo
python app_web.py > inicio_app.log 2>&1

REM Si hay error, mostrar el log
if errorlevel 1 (
    echo.
    echo ERROR AL INICIAR:
    echo ================
    type inicio_app.log
    echo.
    pause
)
