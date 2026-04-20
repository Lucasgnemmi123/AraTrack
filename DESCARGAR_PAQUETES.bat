@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Descargando paquetes para instalacion offline

echo.
echo ═══════════════════════════════════════════════════════════
echo   DESCARGA DE PAQUETES PARA INSTALACION SIN INTERNET
echo ═══════════════════════════════════════════════════════════
echo.
echo  Este script descarga todos los paquetes necesarios a la
echo  carpeta "_paquetes". OneDrive la sincronizara a las demas
echo  PCs para que puedan instalar sin necesitar internet.
echo.
echo  Ejecutar SOLO desde una PC con internet.
echo.
pause

if exist _paquetes (
    echo  Limpiando descarga anterior...
    rmdir /S /Q _paquetes
)
mkdir _paquetes

echo.
echo  Descargando paquetes...
pip download -r requirements.txt -d _paquetes --prefer-binary
if errorlevel 1 (
    echo.
    echo  ERROR: Fallo la descarga. Verifica tu conexion a internet.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   LISTO
echo ═══════════════════════════════════════════════════════════
echo.
echo  Paquetes guardados en: _paquetes\
echo  OneDrive los sincronizara automaticamente a las otras PCs.
echo  Luego en cada PC ejecuta SERVIDOR.bat normalmente.
echo.
pause
