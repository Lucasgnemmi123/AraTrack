@echo off
title Sistema de Viajes DHL - SERVIDOR
cd /d "%~dp0"

REM Establecer modo PRODUCCIÓN
set ARATRACK_ENV=production

echo.
echo ========================================
echo  INICIANDO Sistema de Viajes DHL
echo ========================================
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Iniciar la aplicación
python app_web.py

REM Si llega aquí, la app se detuvo
echo.
echo ========================================
echo  Servidor detenido
echo ========================================
echo.
pause
