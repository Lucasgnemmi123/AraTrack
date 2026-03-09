#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de diagnóstico para verificar imports y configuración"""

import sys
import os

print("="*60)
print("DIAGNÓSTICO DEL SISTEMA")
print("="*60)

# Verificar versión de Python
print(f"\n1. Python: {sys.version}")
print(f"   Ejecutable: {sys.executable}")

# Verificar imports
print("\n2. Verificando dependencias:")
modulos = [
    'flask',
    'reportlab',
    'waitress',
    'sqlite3'
]

for modulo in modulos:
    try:
        __import__(modulo)
        print(f"   ✓ {modulo}")
    except ImportError as e:
        print(f"   ✗ {modulo} - ERROR: {e}")

# Verificar módulos del proyecto
print("\n3. Verificando módulos del proyecto:")
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
        print(f"   ✓ {modulo}")
    except Exception as e:
        print(f"   ✗ {modulo} - ERROR: {e}")

# Verificar base de datos
print("\n4. Verificando base de datos:")
from config import config
print(f"   Entorno: {config.environment}")
print(f"   Base de datos: {config.db_name}")
print(f"   Existe: {os.path.exists(config.db_name)}")

# Verificar templates y static
print("\n5. Verificando estructura:")
carpetas = ['templates', 'static', 'static/css', 'static/js', 'pdfs', 'queries']
for carpeta in carpetas:
    existe = os.path.exists(carpeta)
    print(f"   {'✓' if existe else '✗'} {carpeta}")

print("\n" + "="*60)
print("Diagnóstico completado")
print("="*60 + "\n")
