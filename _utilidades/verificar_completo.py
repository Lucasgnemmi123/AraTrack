#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación EXHAUSTIVA de dependencias del proyecto
"""
import sys
import traceback

print("="*70)
print("VERIFICACIÓN EXHAUSTIVA - Sistema de Viajes DHL")
print("="*70)

errores_encontrados = []
modulos_ok = []

# Test 1: Librerías estándar de Python
print("\n[1/9] Verificando librerías estándar de Python...")
try:
    import sqlite3, os, sys, io, hashlib
    from datetime import datetime
    from functools import wraps
    from typing import List, Dict, Optional
    modulos_ok.append("Librerías estándar")
    print("  ✓ OK")
except Exception as e:
    errores_encontrados.append(("Librerías estándar", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 2: Flask y componentes
print("\n[2/9] Verificando Flask...")
try:
    from flask import Flask, render_template, request, jsonify, send_file
    from flask import redirect, url_for, flash, session
    import flask
    modulos_ok.append(f"Flask {flask.__version__}")
    print(f"  ✓ Flask {flask.__version__}")
except Exception as e:
    errores_encontrados.append(("Flask", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 3: ReportLab completo
print("\n[3/9] Verificando ReportLab...")
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
    from reportlab.lib.units import inch, mm
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    import reportlab
    modulos_ok.append(f"ReportLab {reportlab.Version}")
    print(f"  ✓ ReportLab {reportlab.Version}")
except Exception as e:
    errores_encontrados.append(("ReportLab", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 4: Pandas
print("\n[4/9] Verificando Pandas...")
try:
    import pandas as pd
    import numpy as np
    modulos_ok.append(f"Pandas {pd.__version__}")
    print(f"  ✓ Pandas {pd.__version__}")
    print(f"  ✓ NumPy {np.__version__}")
except Exception as e:
    errores_encontrados.append(("Pandas", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 5: OpenPyXL
print("\n[5/9] Verificando OpenPyXL...")
try:
    import openpyxl
    modulos_ok.append(f"OpenPyXL {openpyxl.__version__}")
    print(f"  ✓ OpenPyXL {openpyxl.__version__}")
except Exception as e:
    errores_encontrados.append(("OpenPyXL", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 6: Waitress
print("\n[6/9] Verificando Waitress...")
try:
    from waitress import serve
    import waitress
    modulos_ok.append(f"Waitress {waitress.__version__}")
    print(f"  ✓ Waitress {waitress.__version__}")
except Exception as e:
    errores_encontrados.append(("Waitress", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 7: python-dotenv
print("\n[7/9] Verificando python-dotenv...")
try:
    import dotenv
    modulos_ok.append("python-dotenv")
    print(f"  ✓ python-dotenv")
except Exception as e:
    errores_encontrados.append(("python-dotenv", str(e)))
    print(f"  ✗ ERROR: {e}")

# Test 8: Módulos del proyecto
print("\n[8/9] Verificando módulos del proyecto...")
modulos_proyecto = [
    'config',
    'db_manager',
    'maestras_manager',
    'pdf_generator',
    'auth_manager',
    'rendiciones_manager'
]

for modulo in modulos_proyecto:
    try:
        __import__(modulo)
        modulos_ok.append(f"  ✓ {modulo}")
        print(f"  ✓ {modulo}")
    except Exception as e:
        errores_encontrados.append((modulo, str(e)))
        print(f"  ✗ {modulo}: {e}")

# Test 9: Base de datos
print("\n[9/9] Verificando base de datos...")
try:
    from config import config
    import os
    db_path = config.get_db_path()
    existe = os.path.exists(db_path)
    
    if existe:
        # Intentar conexión
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        print(f"  ✓ Base de datos: {config.db_name}")
        print(f"  ✓ Entorno: {config.environment}")
        print(f"  ✓ Tablas encontradas: {len(tablas)}")
        
        tablas_requeridas = ['viajes', 'comidas_preparadas', 'usuarios']
        for tabla in tablas_requeridas:
            if tabla in tablas:
                print(f"    ✓ {tabla}")
            else:
                print(f"    ✗ {tabla} NO ENCONTRADA")
                errores_encontrados.append((f"Tabla {tabla}", "No existe en la BD"))
        
        modulos_ok.append("Base de datos")
    else:
        errores_encontrados.append(("Base de datos", f"No encontrada en: {db_path}"))
        print(f"  ✗ Base de datos NO ENCONTRADA: {db_path}")
        
except Exception as e:
    errores_encontrados.append(("Base de datos", str(e)))
    print(f"  ✗ ERROR: {e}")

# RESUMEN FINAL
print("\n" + "="*70)
print("RESUMEN DE VERIFICACIÓN")
print("="*70)

print(f"\n✓ Módulos OK: {len(modulos_ok)}")
print(f"✗ Errores encontrados: {len(errores_encontrados)}")

if errores_encontrados:
    print("\n" + "="*70)
    print("ERRORES DETALLADOS:")
    print("="*70)
    for modulo, error in errores_encontrados:
        print(f"\n✗ {modulo}")
        print(f"  Error: {error}")
    
    print("\n" + "="*70)
    print("SOLUCIONES SUGERIDAS:")
    print("="*70)
    
    # Sugerencias de instalación
    modulos_a_instalar = []
    for modulo, error in errores_encontrados:
        if "No module named" in error:
            if "flask" in error.lower():
                modulos_a_instalar.append("Flask==3.0.0")
            elif "reportlab" in error.lower():
                modulos_a_instalar.append("reportlab==4.0.9")
            elif "pandas" in error.lower():
                modulos_a_instalar.append("pandas")
            elif "openpyxl" in error.lower():
                modulos_a_instalar.append("openpyxl")
            elif "waitress" in error.lower():
                modulos_a_instalar.append("waitress==3.0.2")
            elif "dotenv" in error.lower():
                modulos_a_instalar.append("python-dotenv==1.0.0")
    
    if modulos_a_instalar:
        print("\nEjecuta en la terminal:")
        print(f"  .venv\\Scripts\\activate.bat")
        print(f"  pip install {' '.join(modulos_a_instalar)}")
    
    sys.exit(1)
else:
    print("\n✓✓✓ TODO ESTÁ CORRECTO ✓✓✓")
    print("\nLa aplicación debería iniciar sin problemas.")
    print("Ejecuta: iniciar_web.bat o INICIAR.bat")
    sys.exit(0)
