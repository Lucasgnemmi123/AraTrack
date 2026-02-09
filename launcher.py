"""
Launcher para AraTrack - Aplicación Portable
Abre navegador automáticamente y gestiona recursos embebidos
NO REQUIERE ENTORNO VIRTUAL NI INSTALACIONES EXTERNAS
"""
import sys
import os
import webbrowser
import time
import threading
import socket
import sqlite3

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def check_port_available(port):
    """Verifica si el puerto está disponible"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def setup_environment():
    """Configura el entorno antes de importar Flask"""
    # Configurar rutas para templates y static
    os.environ['FLASK_TEMPLATES_FOLDER'] = resource_path('templates')
    os.environ['FLASK_STATIC_FOLDER'] = resource_path('static')
    
def open_browser():
    """Abre el navegador después de 2 segundos"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000/login')

def main():
    print("=" * 60)
    print("  ARATRACK - Sistema de Gestión de Viajes DHL")
    print("  VERSION PORTABLE - NO REQUIERE INSTALACIONES")
    print("=" * 60)
    print()
    
    # Verificar puerto disponible
    if not check_port_available(5000):
        print("ERROR: Puerto 5000 ya está en uso")
        print("Cierra otras instancias de AraTrack o aplicaciones en puerto 5000")
        input("Presiona Enter para salir...")
        sys.exit(1)
    
    # Obtener IP de red local
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "No disponible"
    
    print("Iniciando servidor web...")
    print()
    print("ACCESO DESDE ESTA PC:")
    print("  http://localhost:5000")
    print()
    print("ACCESO DESDE OTRAS PCs EN LA RED:")
    print(f"  http://{local_ip}:5000")
    print()
    print("IMPORTANTE:")
    print("- NO cierres esta ventana mientras uses la aplicacion")
    print("- El navegador se abrira automaticamente en 2 segundos")
    print("- Para detener: Cierra esta ventana o presiona Ctrl+C")
    print("=" * 60)
    print()
    
    # Configurar entorno
    setup_environment()
    
    # IMPORTANTE: Cambiar al directorio del ejecutable (no la carpeta temporal)
    # Esto asegura que viajes.db se lea FUERA del .exe (debe estar al lado del .exe)
    if getattr(sys, 'frozen', False):
        # Directorio donde está el .exe (no _MEIPASS)
        app_dir = os.path.dirname(sys.executable)
        os.chdir(app_dir)
        print(f"Directorio de trabajo: {app_dir}")
        print()
    
    # Verificar que viajes.db existe (NO la crea, debe estar en la carpeta)
    db_path = 'viajes.db'
    if not os.path.exists(db_path):
        print()
        print("=" * 60)
        print("ERROR: No se encontró la base de datos")
        print("=" * 60)
        print()
        print(f"Buscando: {os.path.abspath(db_path)}")
        print()
        print("SOLUCION:")
        print("  1. Asegúrate de que 'viajes.db' esté en la misma carpeta que AraTrack.exe")
        print("  2. Copia viajes.db desde tu proyecto al lado del ejecutable")
        print("  3. Reinicia AraTrack.exe")
        print()
        input("Presiona Enter para salir...")
        sys.exit(1)
    else:
        print(f"✓ Base de datos encontrada: {os.path.abspath(db_path)}")
        print()
    
    # Abrir navegador en segundo plano
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Importar y ejecutar app
    try:
        print("Cargando aplicacion...")
        from app_web import app
        print("✓ Aplicacion lista")
        print()
        print("Servidor ejecutandose:")
        print(f"  • Esta PC: http://localhost:5000")
        
        # Mostrar IP de red nuevamente
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
            print(f"  • Red local: http://{local_ip}:5000")
        except:
            pass
        
        print()
        print("Presiona Ctrl+C para detener")
        print()
        # Usar Waitress como servidor WSGI de producción
        # IMPORTANTE: Cambiar a 0.0.0.0 para aceptar conexiones de red
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000, threads=10)
    except KeyboardInterrupt:
        print()
        print("Servidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"ERROR al iniciar servidor: {e}")
        print()
        print("Posibles causas:")
        print("- Archivos faltantes en la carpeta")
        print("- Permisos insuficientes")
        print("- Antivirus bloqueando la aplicacion")
        print()
        input("Presiona Enter para salir...")
        sys.exit(1)

if __name__ == '__main__':
    main()
