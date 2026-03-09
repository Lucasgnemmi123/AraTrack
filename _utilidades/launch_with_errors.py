#!/usr/bin/env python
# encoding: utf-8
"""Launcher con captura de errores"""

import sys
import traceback

print("Iniciando aplicación...")
print("="*60)

try:
    # Intentar importar y ejecutar app_web
    print("Importando módulos...")
    
    import app_web
    print("✓ Módulos importados correctamente")
    
    print("\nLa aplicación debería estar corriendo...")
    print("Si no ves mensajes de Waitress/Flask, revisa el código.")
    
except Exception as e:
    print("\n" + "="*60)
    print("ERROR CAPTURADO:")
    print("="*60)
    print(f"\nTipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}\n")
    print("Traceback completo:")
    print("-"*60)
    traceback.print_exc()
    print("="*60)
    
    # Guardar en archivo
    with open('ERROR_INICIO.txt', 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("ERROR AL INICIAR LA APLICACIÓN\n")
        f.write("="*60 + "\n\n")
        f.write(f"Tipo: {type(e).__name__}\n")
        f.write(f"Mensaje: {str(e)}\n\n")
        f.write("Traceback:\n")
        f.write("-"*60 + "\n")
        traceback.print_exc(file=f)
        f.write("\n" + "="*60 + "\n")
    
    print("\nEl error también fue guardado en: ERROR_INICIO.txt")
    sys.exit(1)
