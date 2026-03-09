@echo off
echo ========================================
echo  Diagnostico del Sistema
echo ========================================
echo.

cd /d "%~dp0"

echo [Verificando Python...]
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python NO instalado
    echo    Instalar desde: https://www.python.org/downloads/
) else (
    echo ✓ Python instalado
)

echo.
echo [Verificando Entorno Virtual...]
if exist ".venv\Scripts\python.exe" (
    echo ✓ Entorno virtual existe
    echo    Ruta: %CD%\.venv
) else (
    echo ❌ Entorno virtual NO encontrado
    echo    Ejecuta: reparar_entorno.bat
)

echo.
echo [Verificando Base de Datos...]
if exist "viajes.db" (
    echo ✓ Base de datos produccion: viajes.db
) else (
    echo ⚠ Base de datos produccion NO encontrada
)

if exist "viajes_dev.db" (
    echo ✓ Base de datos desarrollo: viajes_dev.db
) else (
    echo ⚠ Base de datos desarrollo NO encontrada
)

echo.
echo [Verificando Dependencias...]
if exist ".venv\Scripts\python.exe" (
    call .venv\Scripts\activate.bat
    python -c "import flask" 2>nul && echo ✓ Flask instalado || echo ❌ Flask falta
    python -c "import reportlab" 2>nul && echo ✓ ReportLab instalado || echo ❌ ReportLab falta
    python -c "import waitress" 2>nul && echo ✓ Waitress instalado || echo ❌ Waitress falta
) else (
    echo ⚠ No se puede verificar (falta entorno virtual)
)

echo.
echo [Verificando Archivos del Sistema...]
if exist "app_web.py" (echo ✓ app_web.py) else (echo ❌ app_web.py falta)
if exist "config.py" (echo ✓ config.py) else (echo ❌ config.py falta)
if exist "db_manager.py" (echo ✓ db_manager.py) else (echo ❌ db_manager.py falta)
if exist "requirements.txt" (echo ✓ requirements.txt) else (echo ❌ requirements.txt falta)

echo.
echo [Verificando Carpetas...]
if exist "templates" (echo ✓ templates\) else (echo ❌ templates\ falta)
if exist "static" (echo ✓ static\) else (echo ❌ static\ falta)
if exist "queries" (echo ✓ queries\) else (echo ❌ queries\ falta)
if exist "pdfs" (echo ✓ pdfs\) else (echo ⚠ pdfs\ no existe - se creara automaticamente)

echo.
echo ========================================
echo  Diagnostico Completo
echo ========================================
echo.
echo Si hay problemas, ejecuta: reparar_entorno.bat
echo.
pause
