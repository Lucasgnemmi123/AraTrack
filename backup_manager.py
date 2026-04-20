"""
Backup automático de viajes.db a OneDrive cada 2 horas.
Se ejecuta en un hilo en segundo plano mientras el servidor está activo.
"""

import shutil
import threading
import time
import os
from datetime import datetime

# Ruta origen de la base de datos
DB_ORIGEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "viajes.db")

# Ruta destino en OneDrive
DB_DESTINO_DIR = os.path.join(
    os.path.expanduser("~"),
    "OneDrive - DPDHL",
    "Sistema-Viajes-DHL",
    "DHL_Viajes_DB"
)
DB_DESTINO = os.path.join(DB_DESTINO_DIR, "viajes.db")

# Intervalo en segundos (2 horas)
INTERVALO = 2 * 60 * 60

_hilo_backup = None
_detener = threading.Event()


def _realizar_backup():
    """Copia viajes.db al destino en OneDrive."""
    try:
        os.makedirs(DB_DESTINO_DIR, exist_ok=True)
        shutil.copy2(DB_ORIGEN, DB_DESTINO)
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"[Backup] Copia a OneDrive realizada: {ahora}")
    except Exception as e:
        print(f"[Backup] Error al copiar base de datos: {e}")


def _loop_backup():
    """Bucle del hilo: realiza backup inmediato al iniciar y luego cada 2 horas."""
    _realizar_backup()
    while not _detener.wait(timeout=INTERVALO):
        _realizar_backup()


def iniciar():
    """Inicia el hilo de backup en segundo plano."""
    global _hilo_backup
    if not os.path.exists(DB_ORIGEN):
        print("[Backup] No se encontró viajes.db, backup automático no iniciado.")
        return

    destino_disponible = os.path.exists(os.path.dirname(DB_DESTINO_DIR.rstrip(os.sep)))
    if not destino_disponible:
        print("[Backup] OneDrive no disponible, backup automático no iniciado.")
        return

    _detener.clear()
    _hilo_backup = threading.Thread(target=_loop_backup, daemon=True, name="BackupOneDrive")
    _hilo_backup.start()
    print(f"[Backup] Backup automático iniciado. Destino: {DB_DESTINO_DIR}")


def detener():
    """Detiene el hilo de backup."""
    _detener.set()
