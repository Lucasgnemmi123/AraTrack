@echo off
chcp 65001 >nul
title Recreando Entorno Virtual Completo
color 0B
cls

REM ═════════════════════════════════════════════════════════════════════════
REM  RECREAR_ENTORNO.BAT - Limpia y recrea el entorno virtual
REM ═════════════════════════════════════════════════════════════════════════
set "APP_DIR=%~dp0"
set "VENV_DIR=%APP_DIR%.venv"
set "PACKAGES_DIR=%APP_DIR%_paquetes"

echo.
echo ═══════════════════════════════════════════════════════════
echo   RECREACIÓN COMPLETA DEL ENTORNO VIRTUAL
echo ═══════════════════════════════════════════════════════════
echo.
echo  Ubicacion: %VENV_DIR%
echo.
echo  Este proceso eliminara el .venv y lo recreara desde cero.
echo  Los paquetes en _paquetes se mantendran.
echo.
echo  ⏱️  Tiempo estimado: 1-2 minutos
echo.
pause

echo.
echo [1/4] Deteniendo procesos Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 2 /nobreak >nul
echo ✓ Procesos detenidos

echo.
echo [2/4] Eliminando .venv antiguo...
if exist "%VENV_DIR%" (
    rmdir /S /Q "%VENV_DIR%" 2>nul
    timeout /t 1 /nobreak >nul
    if exist "%VENV_DIR%" (
        echo  ⚠️  Intentando con PowerShell...
        powershell -Command "Remove-Item -Path '%VENV_DIR%' -Recurse -Force -ErrorAction SilentlyContinue"
        timeout /t 2 /nobreak >nul
    )
    if exist "%VENV_DIR%" (
        echo  ❌ ERROR: No se pudo eliminar .venv
        echo     Cierra todos los programas y procesos Python
        pause
        exit /b 1
    )
    echo ✓ .venv eliminado
) else (
    echo ℹ️  No había .venv previo
)

echo.
echo [3/4] Creando nuevo entorno virtual...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo crear el entorno virtual
    echo    Verifica que Python esté instalado correctamente
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

echo.
echo [4/4] Instalando dependencias...

REM Verificar si hay paquetes locales
if exist "%PACKAGES_DIR%\*.whl" (
    echo  Instalando desde paquetes locales...
    "%VENV_DIR%\Scripts\pip.exe" install -r "%APP_DIR%requirements.txt" --no-index --find-links="%PACKAGES_DIR%"
) else (
    echo  Descargando e instalando desde internet...
    "%VENV_DIR%\Scripts\pip.exe" install -r "%APP_DIR%requirements.txt" --prefer-binary
)

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Falló la instalación de dependencias
    echo.
    echo Si no tienes internet, ejecuta DESCARGAR_PAQUETES.bat
    echo desde una PC con internet y OneDrive sincronizará los archivos.
    pause
    exit /b 1
)

REM Crear marcador de instalación exitosa
echo Instalado el %date% %time% > "%VENV_DIR%\.instalado_ok"

echo.
echo ═══════════════════════════════════════════════════════════
echo   VERIFICACIÓN DE LIBRERÍAS
echo ═══════════════════════════════════════════════════════════
echo.

"%VENV_DIR%\Scripts\python.exe" -c "import flask; print('  ✓ Flask', flask.__version__)" 2>nul || echo   ❌ Flask
"%VENV_DIR%\Scripts\python.exe" -c "import waitress; print('  ✓ Waitress instalado')" 2>nul || echo   ❌ Waitress
"%VENV_DIR%\Scripts\python.exe" -c "import reportlab; print('  ✓ ReportLab instalado')" 2>nul || echo   ❌ ReportLab
"%VENV_DIR%\Scripts\python.exe" -c "import pandas; print('  ✓ Pandas instalado')" 2>nul || echo   ❌ Pandas

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ ENTORNO RECREADO EXITOSAMENTE
echo ═══════════════════════════════════════════════════════════
echo.
echo Ahora puedes iniciar el servidor con SERVIDOR.bat
echo.
pause
