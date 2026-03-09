"""
Interfaz Gráfica para Control del Servidor AraTrack
Permite iniciar, detener y monitorear el servidor de forma sencilla
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import psutil
import socket
import os
import sys
from pathlib import Path

class ServidorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Servidor AraTrack")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Variables
        self.proceso_servidor = None
        self.hilo_lectura = None
        self.ejecutando = False
        self.puerto = 5000
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_widgets()
        
        # Verificar estado inicial
        self.verificar_estado_inicial()
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)
    
    def configurar_estilo(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Iniciar.TButton', 
                       background='#28a745', 
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Detener.TButton',
                       background='#dc3545',
                       foreground='white', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Limpiar.TButton',
                       background='#ffc107',
                       foreground='black',
                       font=('Segoe UI', 9),
                       padding=5)
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, 
                         text="🚀 Servidor AraTrack", 
                         font=('Segoe UI', 16, 'bold'),
                         fg='#2c3e50')
        titulo.pack(pady=(0, 15))
        
        # Frame de estado
        estado_frame = ttk.LabelFrame(main_frame, text="Estado del Servidor", padding="10")
        estado_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.label_estado = tk.Label(estado_frame,
                                     text="⚫ DETENIDO",
                                     font=('Segoe UI', 12, 'bold'),
                                     fg='#dc3545')
        self.label_estado.pack()
        
        self.label_url = tk.Label(estado_frame,
                                  text="URLs aparecerán aquí al iniciar",
                                  font=('Segoe UI', 9),
                                  fg='#6c757d')
        self.label_url.pack(pady=(5, 0))
        
        # Frame de botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botón Iniciar
        self.btn_iniciar = ttk.Button(botones_frame,
                                      text="▶ INICIAR SERVIDOR",
                                      style='Iniciar.TButton',
                                      command=self.iniciar_servidor,
                                      width=20)
        self.btn_iniciar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Detener
        self.btn_detener = ttk.Button(botones_frame,
                                      text="⬛ DETENER SERVIDOR",
                                      style='Detener.TButton',
                                      command=self.detener_servidor,
                                      width=20,
                                      state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón Limpiar Procesos
        btn_limpiar = ttk.Button(botones_frame,
                                text="🧹 Limpiar Procesos",
                                style='Limpiar.TButton',
                                command=self.limpiar_procesos,
                                width=18)
        btn_limpiar.pack(side=tk.LEFT)
        
        # Frame de log
        log_frame = ttk.LabelFrame(main_frame, text="Log del Servidor", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto para log
        self.texto_log = scrolledtext.ScrolledText(log_frame,
                                                   height=15,
                                                   font=('Consolas', 9),
                                                   bg='#1e1e1e',
                                                   fg='#d4d4d4',
                                                   insertbackground='white')
        self.texto_log.pack(fill=tk.BOTH, expand=True)
        self.texto_log.config(state=tk.DISABLED)
        
        # Botón limpiar log
        btn_limpiar_log = ttk.Button(main_frame,
                                     text="Limpiar Log",
                                     command=self.limpiar_log)
        btn_limpiar_log.pack(pady=(5, 0))
    
    def agregar_log(self, mensaje, color=None):
        """Agrega un mensaje al log"""
        self.texto_log.config(state=tk.NORMAL)
        
        if color:
            tag_name = f"color_{color}"
            self.texto_log.tag_config(tag_name, foreground=color)
            self.texto_log.insert(tk.END, mensaje + "\n", tag_name)
        else:
            self.texto_log.insert(tk.END, mensaje + "\n")
        
        self.texto_log.see(tk.END)
        self.texto_log.config(state=tk.DISABLED)
    
    def limpiar_log(self):
        """Limpia el área de log"""
        self.texto_log.config(state=tk.NORMAL)
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.config(state=tk.DISABLED)
    
    def obtener_ip_local(self):
        """Obtiene la IP local de la máquina"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def verificar_estado_inicial(self):
        """Verifica si el servidor ya está corriendo"""
        if self.verificar_puerto_ocupado():
            self.agregar_log("⚠️ El puerto 5000 ya está en uso", "#ffc107")
            self.agregar_log("Puede haber un servidor corriendo", "#ffc107")
            self.actualizar_estado(True)
    
    def verificar_puerto_ocupado(self):
        """Verifica si el puerto está ocupado"""
        for conn in psutil.net_connections():
            if conn.laddr.port == self.puerto and conn.status == 'LISTEN':
                return True
        return False
    
    def iniciar_servidor(self):
        """Inicia el servidor en un hilo separado"""
        if self.ejecutando:
            self.agregar_log("⚠️ El servidor ya está ejecutándose", "#ffc107")
            return
        
        self.agregar_log("=" * 60, "#4a9eff")
        self.agregar_log("🚀 Iniciando servidor AraTrack...", "#4a9eff")
        self.agregar_log("=" * 60, "#4a9eff")
        
        # Construir comando
        python_exe = Path(".venv/Scripts/python.exe")
        if not python_exe.exists():
            self.agregar_log("❌ ERROR: No se encontró .venv/Scripts/python.exe", "#dc3545")
            self.agregar_log("Ejecuta RECREAR_ENTORNO.bat primero", "#dc3545")
            return
        
        # Configurar variables de entorno
        env = os.environ.copy()
        env['ARATRACK_ENV'] = 'production'
        env['PYTHONUNBUFFERED'] = '1'
        
        try:
            # Iniciar proceso
            self.proceso_servidor = subprocess.Popen(
                [str(python_exe), "app_web.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.ejecutando = True
            self.actualizar_estado(True)
            
            # Iniciar hilo de lectura
            self.hilo_lectura = threading.Thread(target=self.leer_salida, daemon=True)
            self.hilo_lectura.start()
            
            # Mostrar URLs
            ip_local = self.obtener_ip_local()
            urls = f"http://localhost:{self.puerto}  •  http://{ip_local}:{self.puerto}"
            self.label_url.config(text=urls, fg='#28a745')
            
        except Exception as e:
            self.agregar_log(f"❌ ERROR al iniciar: {str(e)}", "#dc3545")
            self.ejecutando = False
            self.actualizar_estado(False)
    
    def leer_salida(self):
        """Lee la salida del proceso del servidor"""
        try:
            for linea in iter(self.proceso_servidor.stdout.readline, ''):
                if not linea:
                    break
                linea = linea.strip()
                if linea:
                    # Colorear según contenido
                    color = None
                    if "ERROR" in linea or "Error" in linea:
                        color = "#dc3545"
                    elif "WARNING" in linea or "Advertencia" in linea:
                        color = "#ffc107"
                    elif "✓" in linea or "Servidor iniciado" in linea:
                        color = "#28a745"
                    elif "http://" in linea:
                        color = "#4a9eff"
                    
                    self.root.after(0, self.agregar_log, linea, color)
        except:
            pass
        finally:
            if self.ejecutando:
                self.root.after(0, self.servidor_detenido)
    
    def detener_servidor(self):
        """Detiene el servidor"""
        if not self.ejecutando:
            self.agregar_log("⚠️ El servidor no está ejecutándose", "#ffc107")
            return
        
        self.agregar_log("⏹️ Deteniendo servidor...", "#ffc107")
        
        try:
            if self.proceso_servidor:
                # Terminar proceso
                self.proceso_servidor.terminate()
                try:
                    self.proceso_servidor.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.proceso_servidor.kill()
                
                self.agregar_log("✓ Servidor detenido correctamente", "#28a745")
        except Exception as e:
            self.agregar_log(f"⚠️ Error al detener: {str(e)}", "#ffc107")
        finally:
            self.servidor_detenido()
    
    def servidor_detenido(self):
        """Actualiza el estado cuando el servidor se detiene"""
        self.ejecutando = False
        self.proceso_servidor = None
        self.actualizar_estado(False)
        self.label_url.config(text="URLs aparecerán aquí al iniciar", fg='#6c757d')
    
    def limpiar_procesos(self):
        """Limpia procesos Python externos (no la GUI ni el servidor actual)"""
        self.agregar_log("🧹 Limpiando procesos Python externos...", "#ffc107")
        
        try:
            # Obtener PID de esta GUI y sus padres
            mi_pid = os.getpid()
            mi_proceso = psutil.Process(mi_pid)
            
            # PIDs a proteger: este proceso y todos sus ancestros
            pids_excluir = {mi_pid}
            
            # Agregar procesos padres (pythonw.exe que lanzó esta GUI)
            try:
                padre = mi_proceso.parent()
                while padre and 'python' in padre.name().lower():
                    pids_excluir.add(padre.pid)
                    padre = padre.parent()
            except:
                pass
            
            # Si hay servidor corriendo desde esta GUI, protegerlo también
            if self.proceso_servidor and self.proceso_servidor.poll() is None:
                pids_excluir.add(self.proceso_servidor.pid)
                self.agregar_log(f"ℹ️ Protegiendo GUI y Servidor activo", "#6c757d")
            else:
                self.agregar_log(f"ℹ️ Protegiendo GUI (PID {mi_pid})", "#6c757d")
            
            procesos_eliminados = 0
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'python' in proc.info['name'].lower():
                        pid = proc.info['pid']
                        if pid not in pids_excluir:
                            # Verificar que no sea parte del árbol de procesos de esta GUI
                            try:
                                proc_obj = psutil.Process(pid)
                                es_hijo = False
                                for protected_pid in pids_excluir:
                                    try:
                                        protected = psutil.Process(protected_pid)
                                        if proc_obj in protected.children(recursive=True):
                                            es_hijo = True
                                            break
                                    except:
                                        pass
                                
                                if not es_hijo:
                                    proc.kill()
                                    procesos_eliminados += 1
                                    self.agregar_log(f"  ✓ Proceso eliminado: PID {pid}", "#6c757d")
                            except:
                                pass
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if procesos_eliminados > 0:
                self.agregar_log(f"✓ {procesos_eliminados} proceso(s) externo(s) eliminado(s)", "#28a745")
            else:
                self.agregar_log("ℹ️ No se encontraron procesos Python externos", "#6c757d")
        
        except Exception as e:
            self.agregar_log(f"⚠️ Error al limpiar procesos: {str(e)}", "#ffc107")
    
    def actualizar_estado(self, corriendo):
        """Actualiza los indicadores de estado"""
        if corriendo:
            self.label_estado.config(text="🟢 EJECUTANDO", fg='#28a745')
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_detener.config(state=tk.NORMAL)
        else:
            self.label_estado.config(text="⚫ DETENIDO", fg='#dc3545')
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_detener.config(state=tk.DISABLED)
    
    def al_cerrar(self):
        """Maneja el cierre de la ventana"""
        if self.ejecutando:
            respuesta = tk.messagebox.askyesno(
                "Servidor Ejecutando",
                "El servidor está ejecutándose.\n¿Deseas detenerlo y cerrar?"
            )
            if respuesta:
                self.detener_servidor()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Función principal"""
    root = tk.Tk()
    app = ServidorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
