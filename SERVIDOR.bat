@echo off
chcp 65001 >nul
cd /d "%~dp0"

REM ═════════════════════════════════════════════════════════════════════════
REM  SERVIDOR.BAT - Sistema de Viajes DHL
REM  Configuración inteligente con instalación offline
REM ═════════════════════════════════════════════════════════════════════════
set "APP_DIR=%~dp0"
set "VENV_DIR=%APP_DIR%.venv"
set "PACKAGES_DIR=%APP_DIR%_paquetes"
set "MARKER_FILE=%VENV_DIR%\.instalado_ok"

REM ── PASO 1: Verificar si ya está todo listo ──────────────────────────────
if exist "%MARKER_FILE%" (
    if exist "%VENV_DIR%\Scripts\pythonw.exe" (
        start "" "%VENV_DIR%\Scripts\pythonw.exe" "%APP_DIR%servidor_gui.py"
        exit /b 0
    )
)

REM ── PASO 2: Configuración inicial ────────────────────────────────────────
echo.
echo ═══════════════════════════════════════════════════════════
echo   SISTEMA DE VIAJES DHL - Configuracion Inicial
echo ═══════════════════════════════════════════════════════════
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python no esta instalado o no esta en el PATH.
    pause
    exit /b 1
)

REM ── PASO 3: Crear entorno virtual ────────────────────────────────────────
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo  [1/3] Creando entorno virtual...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo  ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo  ✓ Entorno virtual creado
) else (
    echo  [1/3] Entorno virtual detectado
)

REM ── PASO 4: Descargar paquetes si no existen ─────────────────────────────
if not exist "%PACKAGES_DIR%\*.whl" (
    echo  [2/3] Descargando paquetes...
    echo  (Esto puede tardar unos minutos)
    
    mkdir "%PACKAGES_DIR%" 2>nul
    "%VENV_DIR%\Scripts\pip.exe" download -r "%APP_DIR%requirements.txt" -d "%PACKAGES_DIR%" --prefer-binary
    
    if errorlevel 1 (
        echo.
        echo  ERROR: No se pudieron descargar los paquetes.
        echo  Posibles causas:
        echo    - No hay conexion a internet
        echo    - Firewall bloqueando Python/pip
        echo.
        echo  SOLUCIÓN: Ejecuta este script en una PC con internet.
        echo  OneDrive sincronizara los paquetes automaticamente.
        pause
        exit /b 1
    )
    echo  ✓ Paquetes descargados ^(%PACKAGES_DIR%^)
) else (
    echo  [2/3] Paquetes ya descargados
)

REM ── PASO 5: Instalar desde paquetes locales ──────────────────────────────
echo  [3/3] Instalando dependencias...
"%VENV_DIR%\Scripts\pip.exe" install -r "%APP_DIR%requirements.txt" --no-index --find-links="%PACKAGES_DIR%"

if errorlevel 1 (
    echo.
    echo  ERROR: Fallo la instalacion de dependencias.
    pause
    exit /b 1
)

REM ── PASO 6: Marcar como instalado ────────────────────────────────────────
echo Instalado el %date% %time% > "%MARKER_FILE%"
echo  ✓ Instalacion completa
echo.
echo  Iniciando servidor...
timeout /t 2 /nobreak >nul

start "" "%VENV_DIR%\Scripts\pythonw.exe" "%APP_DIR%servidor_gui.py"
