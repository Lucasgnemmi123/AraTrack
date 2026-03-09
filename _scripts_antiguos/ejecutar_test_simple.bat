@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python test_simple.py > test_simple_output.txt 2>&1
echo off
type test_simple_output.txt
