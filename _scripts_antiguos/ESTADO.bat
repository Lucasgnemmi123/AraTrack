@echo off
title Estado del Sistema de Viajes DHL
echo.
echo ========================================
echo  ESTADO del Sistema de Viajes DHL
echo ========================================
echo.

REM Verificar si Python está corriendo
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Estado: ENCENDIDO
    echo.
    echo Procesos Python corriendo:
    tasklist /FI "IMAGENAME eq python.exe"
    echo.
    echo Puertos en uso:
    netstat -ano | findstr :5000
) else (
    echo Estado: APAGADO
    echo.
    echo No hay procesos Python corriendo.
)

echo.
echo Para:
echo   - Encender: doble click en ENCENDER.bat
echo   - Apagar:   doble click en APAGAR.bat
echo   - Acceder:  http://localhost:5000
echo.
echo ========================================
pause
