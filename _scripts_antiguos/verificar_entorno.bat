@echo off
echo Probando terminal...
cd /d "%~dp0"
echo Directorio actual: %CD%
echo.

echo Verificando entorno virtual...
dir .venv\Scripts\python.exe
echo.

echo Activando entorno...
call .venv\Scripts\activate.bat
echo.

echo Versión de Python:
python --version
echo.

echo Módulos instalados:
python -m pip list
echo.

echo Presiona cualquier tecla para continuar...
pause
