@echo off
chcp 65001 >nul
echo.
echo ========================================
echo  TEST RAPIDO - Sistema DHL
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar que existe el entorno
if not exist ".venv" (
    echo ERROR: No existe el entorno virtual
    echo.
    echo Ejecuta primero: REPARAR_ENTORNO.bat
    echo.
    pause
    exit /b 1
)

REM Activar entorno
call .venv\Scripts\activate.bat

REM Mostrar info
echo Python: 
python --version
echo.

echo Modulos criticos:
python -c "import flask; print('  OK Flask ' + flask.__version__)"
python -c "import reportlab; print('  OK ReportLab')"
python -c "import waitress; print('  OK Waitress')"
python -c "import sqlite3; print('  OK SQLite3')"
echo.

echo Modulos del proyecto:
python -c "import config; print('  OK config')"
python -c "import db_manager; print('  OK db_manager')"
python -c "import auth_manager; print('  OK auth_manager')"
echo.

echo Base de datos:
if exist "viajes.db" (
    echo   OK - viajes.db existe
) else (
    echo   ADVERTENCIA - viajes.db no encontrada
)
echo.

echo ========================================
echo  Sistema verificado
echo ========================================
echo.
pause
