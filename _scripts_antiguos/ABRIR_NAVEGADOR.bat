@echo off
echo.
echo Abriendo Sistema de Viajes DHL en el navegador...
echo.

REM Verificar si está corriendo
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo ADVERTENCIA: El servidor no esta corriendo.
    echo.
    echo Ejecuta primero: ENCENDER.bat
    echo.
    timeout /t 3
)

REM Abrir navegador
start http://localhost:5000
