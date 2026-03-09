@echo off
chcp 65001 >nul 2>&1
title Generador de PDFs - Documentacion

echo.
echo ========================================
echo  GENERADOR DE PDFs - DOCUMENTACION
echo ========================================
echo.
echo Generando PDFs de toda la documentacion...
echo.

cd /d "%~dp0"

REM Activar entorno virtual y ejecutar generador
call .venv\Scripts\activate.bat
python generar_docs_pdf.py

echo.
echo ========================================
echo.
pause
