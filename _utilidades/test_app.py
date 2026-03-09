import sys
import traceback

print("="*60)
print("VERIFICANDO IMPORTS DE APP_WEB.PY")
print("="*60)

try:
    print("\n1. Importando Flask...")
    from flask import Flask
    print("   ✓ Flask OK")
    
    print("\n2. Importando config...")
    from config import config
    print(f"   ✓ config OK - Entorno: {config.environment}")
    
    print("\n3. Importando db_manager...")
    from db_manager import DBManager
    print("   ✓ db_manager OK")
    
    print("\n4. Importando maestras_manager...")
    from maestras_manager import MaestrasManager
    print("   ✓ maestras_manager OK")
    
    print("\n5. Importando pdf_generator...")
    from pdf_generator import PDFGenerator
    print("   ✓ pdf_generator OK")
    
    print("\n6. Importando auth_manager...")
    from auth_manager import AuthManager
    print("   ✓ auth_manager OK")
    
    print("\n7. Importando rendiciones_manager...")
    import rendiciones_manager
    print("   ✓ rendiciones_manager OK")
    
    print("\n" + "="*60)
    print("TODOS LOS IMPORTS EXITOSOS")
    print("="*60)
    print("\nLa aplicación debería poder iniciar.")
    print("Ejecuta: iniciar_web.bat o iniciar_desarrollo.bat")
    
except Exception as e:
    print("\n" + "="*60)
    print("ERROR ENCONTRADO:")
    print("="*60)
    print(f"\n{type(e).__name__}: {e}\n")
    traceback.print_exc()
    print("\n" + "="*60)
    sys.exit(1)
