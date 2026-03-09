@echo off
echo ========================================
echo  Reparar Entorno Virtual
echo ========================================
echo.
echo Este script recreara el entorno virtual
echo para solucionar problemas de rutas.
echo.
pause

cd /d "%~dp0"

echo.
echo [1/4] Eliminando entorno virtual anterior...
if exist ".venv" (
    rmdir /s /q .venv
    echo    ✓ Entorno anterior eliminado
) else (
    echo    ℹ No habia entorno virtual previo
)

echo.
echo [2/4] Creando nuevo entorno virtual...
python -m venv .venv
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo crear el entorno virtual
    echo.
    echo Soluciones:
    echo   1. Verifica que Python este instalado: python --version
    echo   2. Instala Python desde https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo    ✓ Entorno virtual creado

echo.
echo [3/4] Activando entorno virtual...
call .venv\Scripts\activate.bat
echo    ✓ Entorno activado

echo.
echo [4/4] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Fallo al instalar dependencias
    pause
    exit /b 1
)
echo    ✓ Dependencias instaladas

echo.
echo ========================================
echo  ✅ REPARACION COMPLETADA
echo ========================================
echo.
echo El entorno virtual ha sido reparado exitosamente.
echo Ahora puedes ejecutar:
echo   - iniciar_web.bat         (Produccion)
echo   - iniciar_desarrollo.bat  (Desarrollo)
echo.
pause
