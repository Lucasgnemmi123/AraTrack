@echo off
chcp 65001 >nul
title Recreando Entorno Virtual Completo
color 0B
cls

echo.
echo ═══════════════════════════════════════════════════════════
echo   RECREACIÓN COMPLETA DEL ENTORNO VIRTUAL
echo ═══════════════════════════════════════════════════════════
echo.
echo Este proceso eliminará el .venv actual y creará uno nuevo
echo con todas las dependencias instaladas correctamente.
echo.
echo ⏱️  Tiempo estimado: 2-3 minutos
echo.
pause

echo.
echo [1/5] Eliminando procesos Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 3 /nobreak >nul
echo ✓ Procesos eliminados

echo.
echo [2/5] Eliminando .venv antiguo...
if exist .venv (
    echo Eliminando con PowerShell...
    powershell -Command "Remove-Item -Path '.venv' -Recurse -Force -ErrorAction SilentlyContinue"
    timeout /t 2 /nobreak >nul
    if exist .venv (
        echo ⚠️  Intentando eliminación más agresiva...
        rmdir /S /Q .venv 2>nul
        timeout /t 2 /nobreak >nul
    )
    if exist .venv (
        echo ❌ ERROR: No se pudo eliminar .venv completamente
        echo    Cierra TODAS las ventanas y programas que usen Python
        echo    Luego ejecuta este script nuevamente
        pause
        exit /b 1
    )
    echo ✓ .venv eliminado
) else (
    echo ℹ️  No había .venv previo
)

echo.
echo [3/5] Creando nuevo entorno virtual...
python -m venv .venv
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo crear el entorno virtual
    echo    Verifica que Python esté instalado correctamente
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

echo.
echo [4/5] Actualizando pip...
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
echo ✓ pip actualizado

echo.
echo [5/5] Instalando dependencias desde requirements.txt...
echo.
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Falló la instalación de dependencias
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   VERIFICACIÓN FINAL
echo ═══════════════════════════════════════════════════════════
echo.

echo Verificando Waitress...
.venv\Scripts\python.exe -c "import waitress; print('  ✓ Waitress instalado correctamente')" 2>nul
if errorlevel 1 (
    echo   ❌ Waitress NO está disponible
) else (
    echo   ℹ️  Waitress listo para producción
) 

echo.
echo Verificando Flask...
.venv\Scripts\python.exe -c "import flask; print('  ✓ Flask', flask.__version__, 'instalado')"

echo.
echo Verificando ReportLab...
.venv\Scripts\python.exe -c "import reportlab; print('  ✓ ReportLab instalado')"

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ ENTORNO RECREADO EXITOSAMENTE
echo ═══════════════════════════════════════════════════════════
echo.
echo Ahora puedes iniciar el servidor con:
echo   • INICIAR.bat
echo   • iniciar_web.bat
echo.
pause
