import sys

def test_import(module_name, from_module=None):
    """Test import de un módulo"""
    try:
        if from_module:
            exec(f"from {from_module} import {module_name}")
            print(f"  OK: from {from_module} import {module_name}")
        else:
            __import__(module_name)
            print(f"  OK: import {module_name}")
        return True
    except Exception as e:
        print(f"  ERROR: {module_name} - {e}")
        return False

print("="*70)
print("TEST DE IMPORTS - PASO POR PASO")
print("="*70)

# Test 1: Módulos externos
print("\n1. Flask:")
test_import("flask")
test_import("Flask", "flask")

print("\n2. ReportLab:")
test_import("reportlab")

print("\n3. Pandas:")
test_import("pandas")
test_import("pd", "pandas")

print("\n4. OpenPyXL:")
test_import("openpyxl")

print("\n5. Waitress:")
test_import("waitress")

print("\n6. Python-dotenv:")
test_import("dotenv")

# Test 2: Módulos del proyecto
print("\n7. Config:")
test_import("config")

print("\n8. DB Manager:")
test_import("db_manager")

print("\n9. Auth Manager:")
test_import("auth_manager")

print("\n10. Maestras Manager:")
test_import("maestras_manager")

print("\n11. PDF Generator:")
test_import("pdf_generator")

print("\n12. Rendiciones Manager:")
test_import("rendiciones_manager")

print("\n" + "="*70)
print("FIN DEL TEST")
print("="*70)

input("\nPresiona ENTER para cerrar...")
