@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo.
echo Ejecutando launcher con captura de errores...
echo.

python launch_with_errors.py

if exist "ERROR_INICIO.txt" (
    echo.
    echo ============================================
    echo SE ENCONTRARON ERRORES:
    echo ============================================
    type ERROR_INICIO.txt
    echo.
    echo Los errores fueron guardados en ERROR_INICIO.txt
    pause
) else (
    echo.
    echo La aplicacion inicio correctamente.
)
