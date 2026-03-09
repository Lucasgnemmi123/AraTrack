@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python test_imports.py > diagnostico.txt 2>&1
type diagnostico.txt
