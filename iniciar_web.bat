@echo off
echo ========================================
echo  Sistema de Viajes DHL - Web
echo ========================================
echo.

cd /d "%~dp0"

REM Establecer modo PRODUCCIÓN
set ARATRACK_ENV=production

REM Activar entorno virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: No se encuentra el entorno virtual en .venv
    echo.
    echo Por favor, ejecuta primero: python -m venv .venv
    echo Luego: .venv\Scripts\pip.exe install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Usar siempre el Python del entorno virtual para iniciar la app
echo.
echo ========================================
echo  Iniciando Sistema de Viajes DHL
echo ========================================
echo.
echo Configuracion:
echo   - Entorno: PRODUCCION
echo   - Base de datos: viajes.db
echo   - Puerto: 5000
echo.
echo El servidor mostrara las direcciones de acceso...
echo.

REM Ejecutar usando el Python del entorno virtual
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe app_web.py
) else (
    echo ERROR: No se encontró el entorno virtual. No se puede iniciar la aplicación.
    echo.
    echo Por favor, ejecuta primero: python -m venv .venv
    echo Luego: .venv\Scripts\pip.exe install -r requirements.txt
    echo.
    pause
    exit /b 1
)

pause