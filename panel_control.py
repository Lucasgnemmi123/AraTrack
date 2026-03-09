#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Panel de Control - Sistema de Viajes DHL
Menu interactivo para gestionar el servidor
"""
import subprocess
import socket
import sys
import os
import time
import webbrowser

class PanelControl:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.proceso_servidor = None
        
    def limpiar_pantalla(self):
        """Limpiar la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def obtener_ip_local(self):
        """Obtener IP local"""
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "No disponible"
    
    def verificar_puerto(self):
        """Verificar si el puerto 5000 está en uso"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            return result == 0
        except:
            return False
    
    def mostrar_encabezado(self):
        """Mostrar encabezado del panel"""
        print("\n" + "="*60)
        print("      PANEL DE CONTROL - Sistema de Viajes DHL")
        print("="*60)
        
        # Estado del servidor
        if self.verificar_puerto():
            print("\n  Estado: [ON]  SERVIDOR ENCENDIDO")
        else:
            print("\n  Estado: [OFF] SERVIDOR APAGADO")
        
        # Info de red
        ip_local = self.obtener_ip_local()
        print(f"\n  Acceso LOCAL:    http://localhost:5000")
        print(f"  Acceso desde RED: http://{ip_local}:5000")
        print(f"\n  Usuario: admin | Contrasena: admin123")
        print("\n" + "="*60)
    
    def mostrar_menu(self):
        """Mostrar menu principal"""
        print("\n  OPCIONES:")
        print("  ---------")
        print("  1. Encender servidor")
        print("  2. Apagar servidor")
        print("  3. Abrir en navegador")
        print("  4. Ver estado detallado")
        print("  5. Verificar sistema")
        print("  6. Abrir carpeta del proyecto")
        print("  0. Salir")
        print("\n" + "-"*60)
    
    def encender_servidor(self):
        """Encender el servidor"""
        if self.verificar_puerto():
            print("\n  [!] El servidor ya esta corriendo")
            input("\n  Presiona ENTER para continuar...")
            return
        
        print("\n  Iniciando servidor...")
        print("  -------------------------")
        print("\n  IMPORTANTE:")
        print("  - Se abrira una nueva ventana con el servidor")
        print("  - NO cierres esa ventana mientras uses el sistema")
        print("  - Vuelve a este menu para gestionar el servidor")
        print("\n  Iniciando en 3 segundos...")
        time.sleep(3)
        
        venv_python = os.path.join(self.base_dir, '.venv', 'Scripts', 'python.exe')
        app_web = os.path.join(self.base_dir, 'app_web.py')
        
        # Configurar entorno
        env = os.environ.copy()
        env['ARATRACK_ENV'] = 'production'
        
        # Iniciar en nueva ventana
        if sys.platform == 'win32':
            subprocess.Popen(
                f'start cmd /k "{venv_python}" "{app_web}"',
                shell=True,
                cwd=self.base_dir,
                env=env
            )
        
        print("\n  [OK] Servidor iniciado en nueva ventana")
        print("\n  Esperando 5 segundos...")
        time.sleep(5)
        
        if self.verificar_puerto():
            print("\n  [OK] Servidor funcionando correctamente")
        else:
            print("\n  [!] El servidor puede tardar en iniciar")
            print("     Verifica la ventana del servidor")
        
        input("\n  Presiona ENTER para continuar...")
    
    def apagar_servidor(self):
        """Apagar el servidor"""
        if not self.verificar_puerto():
            print("\n  [i] El servidor no esta corriendo")
            input("\n  Presiona ENTER para continuar...")
            return
        
        print("\n  Deteniendo servidor...")
        
        try:
            # Matar procesos Python
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                             capture_output=True)
            
            print("\n  [OK] Servidor detenido")
            time.sleep(2)
            
        except Exception as e:
            print(f"\n  [!] Error: {e}")
        
        input("\n  Presiona ENTER para continuar...")
    
    def abrir_navegador(self):
        """Abrir navegador"""
        if not self.verificar_puerto():
            print("\n  [!] El servidor no esta corriendo")
            print("\n  Primero enciende el servidor (opcion 1)")
            input("\n  Presiona ENTER para continuar...")
            return
        
        print("\n  Abriendo navegador...")
        webbrowser.open('http://localhost:5000')
        print("\n  [OK] Navegador abierto")
        print("\n  Si no se abrio, ve a: http://localhost:5000")
        input("\n  Presiona ENTER para continuar...")
    
    def ver_estado(self):
        """Ver estado detallado"""
        print("\n  ESTADO DEL SISTEMA")
        print("  ---------------------")
        
        # Servidor
        if self.verificar_puerto():
            print("\n  [+] Servidor: ENCENDIDO (Puerto 5000 en uso)")
        else:
            print("\n  [-] Servidor: APAGADO (Puerto 5000 libre)")
        
        # Base de datos
        db_path = os.path.join(self.base_dir, 'viajes.db')
        if os.path.exists(db_path):
            size = os.path.getsize(db_path) / 1024  # KB
            print(f"\n  [+] Base de datos: viajes.db ({size:.1f} KB)")
        else:
            print("\n  [-] Base de datos: No encontrada")
        
        # Base de datos dev
        db_dev_path = os.path.join(self.base_dir, 'viajes_dev.db')
        if os.path.exists(db_dev_path):
            size_dev = os.path.getsize(db_dev_path) / 1024
            print(f"  [+] Base datos dev: viajes_dev.db ({size_dev:.1f} KB)")
        
        # Entorno virtual
        venv_path = os.path.join(self.base_dir, '.venv')
        if os.path.exists(venv_path):
            print("\n  [+] Entorno virtual: Configurado")
        else:
            print("\n  [-] Entorno virtual: No encontrado")
        
        # IP
        print(f"\n  IP Local: {self.obtener_ip_local()}")
        
        input("\n  Presiona ENTER para continuar...")
    
    def verificar_sistema(self):
        """Verificar sistema"""
        print("\n  VERIFICANDO SISTEMA")
        print("  ----------------------")
        
        venv_python = os.path.join(self.base_dir, '.venv', 'Scripts', 'python.exe')
        
        # Python
        print("\n  [1/4] Python...")
        try:
            result = subprocess.run([venv_python, '--version'], 
                                  capture_output=True, text=True)
            print(f"  [+] {result.stdout.strip()}")
        except:
            print("  [-] Error al verificar Python")
        
        # Flask
        print("\n  [2/4] Flask...")
        try:
            result = subprocess.run([venv_python, '-c', 'import flask; print(flask.__version__)'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  [+] Flask {result.stdout.strip()}")
            else:
                print("  [-] Flask no instalado")
        except:
            print("  [-] Error al verificar Flask")
        
        # ReportLab
        print("\n  [3/4] ReportLab (PDFs)...")
        try:
            result = subprocess.run([venv_python, '-c', 'import reportlab'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  [+] ReportLab instalado")
            else:
                print("  [-] ReportLab no instalado")
        except:
            print("  [-] Error al verificar ReportLab")
        
        # Pandas
        print("\n  [4/4] Pandas (Excel)...")
        try:
            result = subprocess.run([venv_python, '-c', 'import pandas'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  [+] Pandas instalado")
            else:
                print("  [-] Pandas no instalado")
        except:
            print("  [-] Error al verificar Pandas")
        
        print("\n  =======================")
        print("  Verificacion completada")
        input("\n  Presiona ENTER para continuar...")
    
    def abrir_carpeta(self):
        """Abrir carpeta del proyecto"""
        print("\n  Abriendo carpeta del proyecto...")
        if sys.platform == 'win32':
            os.startfile(self.base_dir)
        print("\n  [OK] Carpeta abierta")
        input("\n  Presiona ENTER para continuar...")
    
    def ejecutar(self):
        """Bucle principal del menú"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_menu()
            
            try:
                opcion = input("\n  Selecciona una opción: ").strip()
                
                if opcion == '1':
                    self.encender_servidor()
                elif opcion == '2':
                    self.apagar_servidor()
                elif opcion == '3':
                    self.abrir_navegador()
                elif opcion == '4':
                    self.ver_estado()
                elif opcion == '5':
                    self.verificar_sistema()
                elif opcion == '6':
                    self.abrir_carpeta()
                elif opcion == '0':
                    print("\n  Hasta luego!")
                    time.sleep(1)
                    break
                else:
                    print("\n  [!] Opcion no valida")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n\n  Hasta luego!")
                time.sleep(1)
                break
            except Exception as e:
                print(f"\n  [!] Error: {e}")
                input("\n  Presiona ENTER para continuar...")

def main():
    panel = PanelControl()
    panel.ejecutar()

if __name__ == '__main__':
    main()
