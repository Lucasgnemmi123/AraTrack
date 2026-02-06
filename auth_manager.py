"""
Sistema de Autenticación para AraTrack Pro
Gestión de usuarios con SQLite
"""
import sqlite3
import hashlib
import os
from functools import wraps
from flask import session, redirect, url_for, flash

class AuthManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'viajes.db')
        self.init_users_table()
        self.create_default_user()
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=30.0,
            check_same_thread=False
        )
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_users_table(self):
        """Crear tabla de usuarios si no existe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                email TEXT,
                activo INTEGER DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Tabla de usuarios inicializada")
    
    def hash_password(self, password):
        """Hashear contraseña con SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_user(self):
        """Crear usuario por defecto si no existe"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM usuarios')
        if cursor.fetchone()['count'] == 0:
            # Usuario por defecto: admin / admin123
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, nombre_completo, email)
                VALUES (?, ?, ?, ?)
            ''', ('admin', self.hash_password('admin123'), 'Administrador', 'admin@aratrack.com'))
            
            conn.commit()
            print("Usuario por defecto creado: admin / admin123")
        
        conn.close()
    
    def verify_user(self, username, password):
        """Verificar credenciales de usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, username, nombre_completo, email
            FROM usuarios
            WHERE username = ? AND password_hash = ? AND activo = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    def verify_user_by_username(self, username):
        """Verificar usuario solo por nombre (sin contraseña)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, nombre_completo, email
            FROM usuarios
            WHERE username = ? AND activo = 1
        ''', (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    def create_user(self, username, password, nombre_completo, email=None):
        """Crear nuevo usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO usuarios (username, password_hash, nombre_completo, email)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, nombre_completo, email))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            conn.close()
            return False, "El usuario ya existe"
    
    def get_all_users(self):
        """Obtener lista de todos los usuarios"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, nombre_completo, email, activo, fecha_creacion
            FROM usuarios
            ORDER BY fecha_creacion DESC
        ''')
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def update_password(self, user_id, new_password):
        """Actualizar contraseña de usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(new_password)
        cursor.execute('''
            UPDATE usuarios
            SET password_hash = ?
            WHERE id = ?
        ''', (password_hash, user_id))
        
        conn.commit()
        conn.close()
        return True
    
    def change_user_password(self, user_id, nueva_password):
        """Cambiar contraseña de un usuario (por admin)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(nueva_password)
            cursor.execute('''
                UPDATE usuarios
                SET password_hash = ?
                WHERE id = ?
            ''', (password_hash, user_id))
            
            conn.commit()
            conn.close()
            return True, "Contraseña actualizada"
        except Exception as e:
            print(f"Error al cambiar contraseña: {e}")
            conn.close()
            return False, str(e)
    
    def toggle_user_status(self, user_id):
        """Activar/desactivar usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener estado actual
            cursor.execute('SELECT activo FROM usuarios WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False
            
            nuevo_estado = 0 if row['activo'] else 1
            
            cursor.execute('''
                UPDATE usuarios
                SET activo = ?
                WHERE id = ?
            ''', (nuevo_estado, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error toggle status: {e}")
            conn.close()
            return False
    
    def delete_user(self, user_id):
        """Eliminar usuario de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar que no sea el usuario admin
            cursor.execute('SELECT username FROM usuarios WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False, "Usuario no encontrado"
            
            if row['username'] == 'admin':
                conn.close()
                return False, "No se puede eliminar el usuario admin"
            
            # Eliminar usuario
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            return True, "Usuario eliminado"
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            conn.close()
            return False, str(e)

def login_required(f):
    """Decorator para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
