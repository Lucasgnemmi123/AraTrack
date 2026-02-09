@echo off
echo ============================================
echo   CONSTRUYENDO EJECUTABLE PORTABLE ARATRACK
echo ============================================
echo.

REM Activar entorno virtual si existe, sino usar Python del sistema
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo No se encontro entorno virtual, usando Python del sistema
)

REM Instalar PyInstaller si no esta
pip install pyinstaller

REM Limpiar builds anteriores
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "AraTrack_Portable" rmdir /s /q AraTrack_Portable

REM Crear ejecutable (carpeta con todos los archivos visibles)
echo.
echo Generando aplicacion portable (archivos visibles)...
echo.
pyinstaller --noconfirm ^
    --console ^
    --name "AraTrack" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "queries;queries" ^
    --hidden-import=waitress ^
    --hidden-import=openpyxl ^
    --hidden-import=openpyxl.cell._writer ^
    --hidden-import=openpyxl.styles ^
    --hidden-import=flask ^
    --hidden-import=werkzeug ^
    --hidden-import=jinja2 ^
    --hidden-import=sqlite3 ^
    --hidden-import=db_manager ^
    --hidden-import=maestras_manager ^
    --hidden-import=auth_manager ^
    --hidden-import=pdf_generator ^
    --collect-all openpyxl ^
    --collect-all flask ^
    launcher.py

REM Crear carpeta portable con todo lo necesario
REM Crear carpeta portable con todos los archivos visibles
echo.
echo Creando carpeta portable con todos los archivos...
if exist "AraTrack_Portable" rmdir /s /q AraTrack_Portable
xcopy "dist\AraTrack" "AraTrack_Portable\" /E /I /Y

REM Copiar módulos Python locales a _internal (CRÍTICO para que funcione)
echo Copiando modulos Python locales...
copy db_manager.py AraTrack_Portable\_internal\
copy maestras_manager.py AraTrack_Portable\_internal\
copy auth_manager.py AraTrack_Portable\_internal\
copy pdf_generator.py AraTrack_Portable\_internal\
copy app_web.py AraTrack_Portable\_internal\

REM Copiar base de datos al mismo nivel que el ejecutable
echo Copiando base de datos...
if exist "viajes.db" copy viajes.db AraTrack_Portable\

echo.
echo ============================================
echo   CARPETA PORTABLE CREADA: AraTrack_Portable
echo ============================================
echo.
echo CONTENIDO:
echo - AraTrack.exe (ejecutable principal)
echo - viajes.db (base de datos - VISIBLE y editable)
echo - Todos los archivos DLL y dependencias
echo - Carpetas: templates, static, queries
echo.
echo INSTRUCCIONES:
echo 1. Comprime la carpeta "AraTrack_Portable"
echo 2. Enviala a otro usuario
echo 3. El usuario descomprime y ejecuta AraTrack.exe
echo 4. La base de datos viajes.db es visible y se puede abrir con DB Browser
echo.
echo NO NECESITA:
echo - Instalar Python
echo - Instalar librerias
echo - Configurar nada
echo.
pause
