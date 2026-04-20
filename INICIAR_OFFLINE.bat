@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Sistema Viajes DHL

REM ═════════════════════════════════════════════════════════════════════════
REM  SERVIDOR - Sistema de Viajes DHL
REM  MODO OFFLINE - Sin conexión a internet
REM ═════════════════════════════════════════════════════════════════════════

set "APP_DIR=%~dp0"
set "VENV_DIR=%APP_DIR%.venv"

REM ── Configuración ambiente OFFLINE ───────────────────────────────────────
set PIP_NO_INDEX=1
set PIP_FIND_LINKS=%APP_DIR%_paquetes
set PIP_DISABLE_PIP_VERSION_CHECK=1
set PYTHONDONTWRITEBYTECODE=1

REM ── Verificar que existe entorno virtual ─────────────────────────────────
if not exist "%VENV_DIR%\Scripts\pythonw.exe" (
    color 0C
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   ERROR: Entorno virtual no encontrado
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo  El entorno virtual no esta configurado.
    echo.
    echo  SOLUCIÓN:
    echo    1. Ejecuta: RECREAR_ENTORNO.bat
    echo    2. Luego vuelve a ejecutar este archivo
    echo.
    pause
    exit /b 1
)

REM ── Verificar que existe la BD ───────────────────────────────────────────
if not exist "C:\DHL_Viajes_DB\viajes.db" (
    color 0E
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   ADVERTENCIA: Base de datos no encontrada
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo  No se encuentra: C:\DHL_Viajes_DB\viajes.db
    echo.
    echo  La aplicacion se iniciara pero no tendra datos.
    echo.
    timeout /t 5
)

REM ── Iniciar servidor ─────────────────────────────────────────────────────
cls
color 0A
echo.
echo ═══════════════════════════════════════════════════════════
echo   SISTEMA DE VIAJES DHL
echo ═══════════════════════════════════════════════════════════
echo.
echo  Estado: Iniciando...
echo  Base de datos: C:\DHL_Viajes_DB\viajes.db
echo  Puerto: 5000
echo  URL: http://localhost:5000
echo.
echo  MODO OFFLINE: Sin conexion a internet
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM ── Iniciar con pythonw.exe (sin consola adicional) ──────────────────────
start "" "%VENV_DIR%\Scripts\pythonw.exe" "%APP_DIR%servidor_gui.py"

REM Esperar 3 segundos y verificar si se inició
timeout /t 3 /nobreak >nul

REM Verificar si el proceso está corriendo
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo  ✓ Servidor iniciado correctamente
    echo.
    echo  La aplicacion se abrira automaticamente en tu navegador.
    echo  Este mensaje se cerrara solo.
    timeout /t 5 /nobreak >nul
    exit /b 0
) else (
    color 0C
    echo  ERROR: El servidor no se inició correctamente
    echo.
    echo  Revisa el archivo de log para mas detalles.
    pause
    exit /b 1
)
