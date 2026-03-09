@echo off
echo ========================================
echo  Sistema de Viajes DHL
echo  Instalacion Portable
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar que Python este instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python 3.12 desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Eliminar entorno virtual anterior si existe
if exist ".venv" (
    echo Eliminando entorno virtual anterior...
    rmdir /s /q .venv
    echo.
)

REM Crear nuevo entorno virtual
echo Creando entorno virtual local...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo OK - Entorno virtual creado
echo.

REM Actualizar pip
echo Actualizando pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
echo.

REM Instalar dependencias
echo Instalando dependencias desde requirements.txt...
.venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo.

echo ========================================
echo  Instalacion Completada!
echo ========================================
echo.
echo El proyecto esta listo para ejecutar.
echo Ahora puedes:
echo   1. Ejecutar iniciar_web.bat para iniciar el servidor web
echo   2. Copiar toda esta carpeta a otra PC con Python 3.12
echo.
echo IMPORTANTE: Si copias a otra PC, ejecuta este script nuevamente
echo para recrear el entorno virtual en la nueva ubicacion.
echo.

pause
