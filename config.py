"""
Configuración del Sistema de Viajes DHL
Permite separar entornos de desarrollo y producción
"""
import os
import sys

class Config:
    """Configuración centralizada de la aplicación"""
    
    def __init__(self):
        # Detectar si es ejecutable empaquetado o desarrollo
        self.is_frozen = getattr(sys, 'frozen', False)
        
        # Obtener directorio base
        if self.is_frozen:
            # Ejecutable empaquetado: usar directorio del .exe
            self.base_dir = os.path.dirname(sys.executable)
        else:
            # Desarrollo: usar directorio del script
            self.base_dir = os.path.dirname(__file__)
        
        # Modo de ejecución: 'development' o 'production'
        # Puedes cambiarlo con variable de entorno: set ARATRACK_ENV=production
        self.environment = os.getenv('ARATRACK_ENV', 'development')
        
        # Configuración de base de datos
        if self.environment == 'production':
            self.db_name = 'viajes.db'
            self.port = 5000
        else:
            # Desarrollo: usar base de datos separada
            self.db_name = 'viajes_dev.db'
            self.port = 5000
        
        self.db_path = os.path.join(self.base_dir, self.db_name)
        
        # Configuración del servidor
        self.host = os.getenv('ARATRACK_HOST', '0.0.0.0')
        self.threads = int(os.getenv('ARATRACK_THREADS', '10'))
        
        # Secret key para Flask
        self.secret_key = os.getenv('ARATRACK_SECRET_KEY', 'aratrack-pro-2025-secure-key')
        
    def is_development(self):
        """Verifica si está en modo desarrollo"""
        return self.environment == 'development'
    
    def is_production(self):
        """Verifica si está en modo producción"""
        return self.environment == 'production'
    
    def get_db_path(self):
        """Retorna la ruta completa de la base de datos"""
        return self.db_path
    
    def get_port(self):
        """Retorna el puerto configurado"""
        return self.port
    
    def info(self):
        """Muestra información de configuración"""
        return {
            'environment': self.environment,
            'db_path': self.db_path,
            'port': self.port,
            'host': self.host,
            'base_dir': self.base_dir,
            'is_frozen': self.is_frozen
        }

# Instancia global de configuración
config = Config()
