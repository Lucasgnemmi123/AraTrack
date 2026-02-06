@echo off
echo ========================================
echo  Sistema de Viajes DHL - Web
echo ========================================
echo.

cd /d "%~dp0"

REM Activar entorno virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: No se encuentra el entorno virtual
    echo Por favor crea el entorno virtual primero con: python -m venv .venv
    pause
    exit /b 1
)

REM Verificar que Flask esté instalado
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Instalando Flask...
    pip install Flask
)

REM Iniciar servidor Flask
echo.
echo ========================================
echo  Iniciando Sistema de Viajes DHL
echo ========================================
echo.
echo Modo: RED LOCAL (5 usuarios)
echo Base de datos: SQLite
echo.
echo El servidor mostrara las direcciones de acceso...
echo.

python app_web.py

pause
