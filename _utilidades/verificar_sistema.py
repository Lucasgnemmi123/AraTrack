import sys
import os

with open('estado_sistema.txt', 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("ESTADO DEL SISTEMA - " + str(__file__) + "\n")
    f.write("="*60 + "\n\n")
    
    # Python
    f.write(f"Python: {sys.version}\n")
    f.write(f"Ejecutable: {sys.executable}\n\n")
    
    # Verificar dependencias
    f.write("DEPENDENCIAS:\n")
    modulos = ['flask', 'reportlab', 'waitress', 'sqlite3']
    for mod in modulos:
        try:
            m = __import__(mod)
            v = getattr(m, '__version__', 'OK')
            f.write(f"  ✓ {mod}: {v}\n")
        except Exception as e:
            f.write(f"  ✗ {mod}: {e}\n")
    
    f.write("\nMÓDULOS DEL PROYECTO:\n")
    modulos_proyecto = ['config', 'db_manager', 'maestras_manager', 'pdf_generator', 'auth_manager', 'rendiciones_manager']
    for mod in modulos_proyecto:
        try:
            __import__(mod)
            f.write(f"  ✓ {mod}\n")
        except Exception as e:
            f.write(f"  ✗ {mod}: {e}\n")
    
    # Base de datos
    f.write("\nBASE DE DATOS:\n")
    from config import config
    f.write(f"  Entorno: {config.environment}\n")
    f.write(f"  DB: {config.db_name}\n")
    f.write(f"  Existe: {os.path.exists(config.db_name)}\n")
    
    f.write("\n" + "="*60 + "\n")
    f.write("VERIFICACIÓN COMPLETADA\n")
    f.write("="*60 + "\n")

print("Verificación guardada en: estado_sistema.txt")
