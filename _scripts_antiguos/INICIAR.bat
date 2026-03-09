@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   Iniciando Sistema de Viajes DHL
echo ========================================
echo.

REM Activar entorno y ejecutar
call .venv\Scripts\activate.bat
python -u app_web.py

REM Si llega aquí, hubo un error
echo.
echo La aplicación se detuvo. Presiona cualquier tecla...
pause >nul
