@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python verificar_completo.py > resultado_verificacion.txt 2>&1
type resultado_verificacion.txt
echo.
echo Los resultados han sido guardados en: resultado_verificacion.txt
pause
