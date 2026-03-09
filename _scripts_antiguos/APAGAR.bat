@echo off
title Apagar Sistema de Viajes DHL
echo.
echo ========================================
echo  APAGANDO Sistema de Viajes DHL
echo ========================================
echo.
echo Deteniendo procesos Python...

REM Detener todos los procesos Python
taskkill /F /IM python.exe >nul 2>&1

if %errorlevel% equ 0 (
    echo   OK - Servidor detenido correctamente
) else (
    echo   INFO - No habia procesos Python corriendo
)

echo.
echo ========================================
echo  Servidor apagado
echo ========================================
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
