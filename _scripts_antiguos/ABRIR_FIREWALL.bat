@echo off
echo.
echo ========================================
echo  Configurar Firewall para Acceso Remoto
echo ========================================
echo.
echo Este script abrira el puerto 5000 en el Firewall de Windows
echo para permitir acceso desde otras PCs en la red.
echo.
echo NOTA: Requiere permisos de Administrador
echo.
pause

echo.
echo Agregando regla al Firewall...

REM Eliminar regla anterior si existe
netsh advfirewall firewall delete rule name="Sistema Viajes DHL - Puerto 5000" >nul 2>&1

REM Agregar nueva regla
netsh advfirewall firewall add rule name="Sistema Viajes DHL - Puerto 5000" dir=in action=allow protocol=TCP localport=5000

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  FIREWALL CONFIGURADO CORRECTAMENTE
    echo ========================================
    echo.
    echo El puerto 5000 ahora esta abierto para acceso desde la red.
    echo.
    echo Otras PCs pueden acceder usando:
    echo   http://TU-IP:5000
    echo.
    echo Para ver tu IP ejecuta: ipconfig
) else (
    echo.
    echo ========================================
    echo  ERROR: No se pudo configurar
    echo ========================================
    echo.
    echo Ejecuta este script como Administrador:
    echo   1. Click derecho sobre el archivo
    echo   2. Selecciona "Ejecutar como administrador"
)

echo.
pause
