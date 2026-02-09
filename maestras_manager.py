import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class MaestrasManager:
    """Clase para manejar las tablas maestras (choferes, administrativos, casinos)"""
    
    def __init__(self, db_path: str = "viajes.db"):
        self.db_path = db_path
    
    def _get_connection(self):
        """Obtener conexión optimizada para concurrencia"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=30.0,  # Mayor timeout para esperar en caso de bloqueo
            check_same_thread=False,
            isolation_level=None  # Modo autocommit para mejor concurrencia
        )
        # Habilitar WAL mode para mejor concurrencia
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA busy_timeout=30000')
        return conn
    
    def buscar_choferes_por_nombre(self, nombre: str) -> List[Dict]:
        """Buscar choferes por nombre (búsqueda parcial, insensible a mayúsculas)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Buscar nombres que contengan la cadena de búsqueda
        query = """
        SELECT id, nombre, celular, rut 
        FROM maestras_choferes 
        WHERE UPPER(nombre) LIKE UPPER(?)
        ORDER BY nombre
        LIMIT 10
        """
        
        cursor.execute(query, (f"%{nombre}%",))
        results = cursor.fetchall()
        
        choferes = []
        for row in results:
            choferes.append({
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2],
                'rut': row[3]
            })
        
        conn.close()
        return choferes
    
    def buscar_administrativos_por_nombre(self, nombre: str) -> List[Dict]:
        """Buscar administrativos por nombre (búsqueda parcial, insensible a mayúsculas)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, nombre 
        FROM maestras_administrativos 
        WHERE UPPER(nombre) LIKE UPPER(?)
        ORDER BY nombre
        LIMIT 10
        """
        
        cursor.execute(query, (f"%{nombre}%",))
        results = cursor.fetchall()
        
        administrativos = []
        for row in results:
            administrativos.append({
                'id': row[0],
                'nombre': row[1]
            })
        
        conn.close()
        return administrativos
    
    def buscar_casino_por_codigo(self, codigo: int) -> Optional[Dict]:
        """Buscar casino por código de costo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT codigo_costo, casino, ruta
        FROM maestras_casinos 
        WHERE codigo_costo = ?
        """
        
        cursor.execute(query, (codigo,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'codigo_costo': result[0],
                'casino': result[1],
                'ruta': result[2]
            }
        return None
    
    def obtener_todos_casinos(self) -> List[Dict]:
        """Obtener todos los casinos ordenados por nombre"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, codigo_costo, casino, ruta 
        FROM maestras_casinos 
        ORDER BY casino ASC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'codigo_costo': row[1],
                'casino': row[2],
                'ruta': row[3]
            }
            for row in results
        ]
    
    def agregar_casino_si_no_existe(self, codigo_costo: int, casino: str, ruta: str) -> bool:
        """Agregar casino si no existe (basado en código de costo)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si ya existe
            cursor.execute("SELECT 1 FROM maestras_casinos WHERE codigo_costo = ?", (codigo_costo,))
            if cursor.fetchone():
                conn.close()
                return False  # Ya existe
            
            # Agregar nuevo casino
            cursor.execute("""
                INSERT INTO maestras_casinos (codigo_costo, casino, ruta)
                VALUES (?, ?, ?)
            """, (codigo_costo, casino, ruta))
            
            conn.commit()
            conn.close()
            return True  # Se agregó con éxito
            
        except Exception as e:
            conn.close()
            print(f"Error al agregar casino: {e}")
            return False
    
    def agregar_chofer_si_no_existe(self, nombre: str, telefono: str, rut: str) -> bool:
        """Agregar chofer si no existe (basado en RUT)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT id FROM maestras_choferes WHERE rut = ?", (rut,))
        if cursor.fetchone():
            conn.close()
            return False  # Ya existe
        
        # Agregar nuevo chofer
        cursor.execute("""
        INSERT INTO maestras_choferes (nombre, celular, rut)
        VALUES (?, ?, ?)
        """, (nombre, telefono, rut))
        
        conn.commit()
        conn.close()
        return True  # Agregado exitosamente
    
    def agregar_administrativo_si_no_existe(self, nombre: str) -> bool:
        """Agregar administrativo si no existe (basado en nombre)"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT id FROM maestras_administrativos WHERE UPPER(nombre) = UPPER(?)", (nombre,))
        if cursor.fetchone():
            conn.close()
            return False  # Ya existe
        
        # Agregar nuevo administrativo
        cursor.execute("""
        INSERT INTO maestras_administrativos (nombre)
        VALUES (?)
        """, (nombre,))
        
        conn.commit()
        conn.close()
        return True  # Agregado exitosamente
    
    def obtener_todos_los_choferes(self) -> List[Dict]:
        """Obtener todos los choferes"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, celular, rut FROM maestras_choferes ORDER BY nombre")
        results = cursor.fetchall()
        
        choferes = []
        for row in results:
            choferes.append({
                'id': row[0],
                'nombre': row[1],
                'telefono': row[2],
                'rut': row[3]
            })
        
        conn.close()
        return choferes
    
    def obtener_todos_centros_costo(self) -> List[Dict]:
        """Obtener todos los centros de costo (maestras_casinos) ordenados por código"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, codigo_costo, casino, ruta 
            FROM maestras_casinos 
            ORDER BY codigo_costo ASC
        """)
        results = cursor.fetchall()
        
        centros = []
        for row in results:
            centros.append({
                'id': row[0],
                'codigo_costo': row[1],
                'casino': row[2],
                'ruta': row[3]
            })
        
        conn.close()
        return centros
    
    def obtener_todos_los_administrativos(self) -> List[Dict]:
        """Obtener todos los administrativos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre FROM maestras_administrativos ORDER BY nombre")
        results = cursor.fetchall()
        
        administrativos = []
        for row in results:
            administrativos.append({
                'id': row[0],
                'nombre': row[1]
            })
        
        conn.close()
        return administrativos
    
    def crear_centro_costo(self, codigo_costo: str, casino: str, ruta: str = "") -> bool:
        """Crear un nuevo centro de costo en maestras_casinos"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM maestras_casinos WHERE codigo_costo = ?", (codigo_costo,))
            if cursor.fetchone():
                conn.close()
                return False
            
            cursor.execute("""
                INSERT INTO maestras_casinos (codigo_costo, casino, ruta)
                VALUES (?, ?, ?)
            """, (codigo_costo, casino, ruta))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creando centro de costo: {e}")
            return False
    
    def crear_chofer(self, nombre: str, rut: str, celular: str = "") -> bool:
        """Crear un nuevo chofer en maestras_choferes"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM maestras_choferes WHERE rut = ?", (rut,))
            if cursor.fetchone():
                conn.close()
                return False
            
            cursor.execute("""
                INSERT INTO maestras_choferes (nombre, celular, rut)
                VALUES (?, ?, ?)
            """, (nombre, celular, rut))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creando chofer: {e}")
            return False
    
    def crear_administrativo(self, nombre: str) -> bool:
        """Crear un nuevo administrativo en maestras_administrativos"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM maestras_administrativos WHERE nombre = ?", (nombre,))
            if cursor.fetchone():
                conn.close()
                return False
            
            cursor.execute("""
                INSERT INTO maestras_administrativos (nombre)
                VALUES (?)
            """, (nombre,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creando administrativo: {e}")
            return False
    
    def listar_administrativos_nombres(self) -> List[str]:
        """Obtener solo los nombres de todos los administrativos"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT nombre FROM maestras_administrativos ORDER BY nombre")
        results = cursor.fetchall()
        
        nombres = [row[0] for row in results]
        
        conn.close()
        return nombres
    
    # ========== MÉTODOS DE ACTUALIZACIÓN ==========
    def actualizar_casino(self, casino_id: int, codigo_costo: int, casino: str, ruta: str) -> bool:
        """Actualizar un casino existente"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_casinos 
                SET codigo_costo = ?, casino = ?, ruta = ?
                WHERE id = ?
            """, (codigo_costo, casino, ruta, casino_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error al actualizar casino: {e}")
            return False
    
    def actualizar_chofer(self, chofer_id: int, nombre: str, telefono: str, rut: str) -> bool:
        """Actualizar un chofer existente"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_choferes 
                SET nombre = ?, celular = ?, rut = ?
                WHERE id = ?
            """, (nombre, telefono, rut, chofer_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error al actualizar chofer: {e}")
            return False
    
    def actualizar_administrativo(self, admin_id: int, nombre: str) -> bool:
        """Actualizar un administrativo existente"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_administrativos 
                SET nombre = ?
                WHERE id = ?
            """, (nombre, admin_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error al actualizar administrativo: {e}")
            return False
    
    # ====== MÉTODOS DE ACTUALIZACIÓN POR NOMBRE/CÓDIGO ======
    
    def actualizar_centro_costo_por_codigo(self, codigo_costo: str, casino: str, ruta: str = "") -> bool:
        """Actualizar un centro de costo por su código"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_casinos 
                SET casino = ?, ruta = ?
                WHERE codigo_costo = ?
            """, (casino, ruta, codigo_costo))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.close()
            print(f"Error al actualizar centro de costo: {e}")
            return False
    
    def actualizar_chofer_por_nombre(self, nombre: str, rut: str, celular: str = "") -> bool:
        """Actualizar un chofer por su nombre"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_choferes 
                SET rut = ?, celular = ?
                WHERE nombre = ?
            """, (rut, celular, nombre))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.close()
            print(f"Error al actualizar chofer: {e}")
            return False
    
    def actualizar_administrativo_por_nombre(self, nombre_original: str, nombre_nuevo: str) -> bool:
        """Actualizar un administrativo por su nombre"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE maestras_administrativos 
                SET nombre = ?
                WHERE nombre = ?
            """, (nombre_nuevo, nombre_original))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            conn.close()
            print(f"Error al actualizar administrativo: {e}")
            return False
    
    def obtener_chofer_por_nombre(self, nombre: str) -> Optional[Dict]:
        """Obtener datos de un chofer por su nombre"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT nombre, rut, celular
                FROM maestras_choferes
                WHERE nombre = ?
            """, (nombre,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'nombre': row[0],
                    'rut': row[1],
                    'celular': row[2]
                }
            return None
        except Exception as e:
            conn.close()
            print(f"Error al obtener chofer: {e}")
            return None
            
    def obtener_ultimo_viaje_por_numero(self, numero_viaje: str) -> Optional[Dict]:
        """Obtener el último registro de un número de viaje específico"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT * FROM viajes 
        WHERE numero_viaje = ?
        ORDER BY created_at DESC
        LIMIT 1
        """
        
        cursor.execute(query, (numero_viaje,))
        result = cursor.fetchone()
        
        if result:
            # Obtener nombres de las columnas
            cursor.execute("PRAGMA table_info(viajes)")
            columns = [row[1] for row in cursor.fetchall()]
            # Crear diccionario con los datos
            conn.close()
            return dict(zip(columns, result))
        
        conn.close()
        return None

    def obtener_viajes_unicos(self) -> List[Dict]:
        """Obtener números de viaje únicos con el último registro de cada uno"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            v.numero_viaje,
            v.conductor,
            v.fecha,
            COUNT(DISTINCT v.costo_codigo) as total_centros_costo,
            GROUP_CONCAT(DISTINCT v.costo_codigo) as centros_costo
        FROM viajes v
        GROUP BY v.numero_viaje
        ORDER BY v.numero_viaje DESC
        LIMIT 100
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        viajes = []
        for row in results:
            viajes.append({
                'numero_viaje': row[0],
                'conductor': row[1] or 'Sin conductor',
                'fecha': row[2] or 'Sin fecha',
                'total_centros_costo': row[3],
                'centros_costo': row[4]
            })
        
        conn.close()
        return viajes
    
    def obtener_ultimo_registro_viaje(self, numero_viaje: str) -> Dict:
        """Obtener el último registro de un viaje para usar como plantilla"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Obtener el último registro de este viaje (datos comunes)
        query = """
        SELECT * FROM viajes 
        WHERE numero_viaje = ?
        ORDER BY id DESC
        LIMIT 1
        """
        cursor.execute(query, (numero_viaje,))
        result = cursor.fetchone()
        
        if result:
            # Obtener nombres de las columnas
            cursor.execute("PRAGMA table_info(viajes)")
            columns = [row[1] for row in cursor.fetchall()]
            conn.close()
            return dict(zip(columns, result))
        
        conn.close()
        return {}
    
    def obtener_registros_viaje_por_centros(self, numero_viaje: str) -> List[Dict]:
        """Obtener todos los registros de un viaje agrupados por centro de costo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT DISTINCT
            v.costo_codigo,
            v.casino,
            COUNT(c.id) as total_comidas
        FROM viajes v
        LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje 
            AND v.costo_codigo = c.numero_centro_costo
        WHERE v.numero_viaje = ?
        GROUP BY v.costo_codigo
        ORDER BY v.costo_codigo
        """
        cursor.execute(query, (numero_viaje,))
        results = cursor.fetchall()
        
        registros = []
        for row in results:
            registros.append({
                'costo_codigo': row[0],
                'casino': row[1] or 'Sin casino',
                'total_comidas': row[2]
            })
        
        conn.close()
        return registros

    def buscar_viajes_con_centros_costo(self, termino_busqueda: str = None) -> List[Dict]:
        """Buscar viajes únicos con sus centros de costo y comidas"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if termino_busqueda:
            # Búsqueda por número de viaje o centro de costo
            query = """
            SELECT DISTINCT 
                v.numero_viaje,
                v.costo_codigo,
                v.casino,
                v.conductor,
                v.administrativo_responsable,
                COUNT(c.id) as total_comidas
            FROM viajes v
            LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje 
                AND v.costo_codigo = c.numero_centro_costo
            WHERE v.numero_viaje LIKE ? OR v.costo_codigo LIKE ?
            GROUP BY v.numero_viaje, v.costo_codigo
            ORDER BY v.numero_viaje DESC, v.costo_codigo
            LIMIT 20
            """
            cursor.execute(query, (f"%{termino_busqueda}%", f"%{termino_busqueda}%"))
        else:
            # Obtener todos los viajes únicos con centros de costo
            query = """
            SELECT DISTINCT 
                v.numero_viaje,
                v.costo_codigo,
                v.casino,
                v.conductor,
                v.administrativo_responsable,
                COUNT(c.id) as total_comidas
            FROM viajes v
            LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje 
                AND v.costo_codigo = c.numero_centro_costo
            GROUP BY v.numero_viaje, v.costo_codigo
            ORDER BY v.numero_viaje DESC, v.costo_codigo
            LIMIT 50
            """
            cursor.execute(query)
            
        results = cursor.fetchall()
        
        viajes = []
        for row in results:
            viajes.append({
                'numero_viaje': row[0],
                'costo_codigo': row[1], 
                'casino': row[2],
                'conductor': row[3],
                'administrativo_responsable': row[4],
                'total_comidas': row[5]
            })
        
        conn.close()
        return viajes
    
    def obtener_viaje_completo_por_numero_y_centro(self, numero_viaje: str, centro_costo: str) -> Dict:
        """Obtener todos los datos de un viaje específico por número y centro de costo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Obtener datos del viaje
        query_viaje = """
        SELECT * FROM viajes 
        WHERE numero_viaje = ? AND costo_codigo = ?
        ORDER BY id DESC
        LIMIT 1
        """
        cursor.execute(query_viaje, (numero_viaje, centro_costo))
        viaje_result = cursor.fetchone()
        
        if not viaje_result:
            conn.close()
            return {}
            
        # Obtener nombres de las columnas de viajes
        cursor.execute("PRAGMA table_info(viajes)")
        viaje_columns = [row[1] for row in cursor.fetchall()]
        viaje_data = dict(zip(viaje_columns, viaje_result))
        
        # Obtener comidas asociadas
        query_comidas = """
        SELECT * FROM comidas_preparadas 
        WHERE numero_viaje = ? AND numero_centro_costo = ?
        ORDER BY id
        """
        cursor.execute(query_comidas, (numero_viaje, centro_costo))
        comidas_results = cursor.fetchall()
        
        comidas = []
        if comidas_results:
            cursor.execute("PRAGMA table_info(comidas_preparadas)")
            comidas_columns = [row[1] for row in cursor.fetchall()]
            for comida_row in comidas_results:
                comidas.append(dict(zip(comidas_columns, comida_row)))
        
        conn.close()
        
        return {
            'viaje_data': viaje_data,
            'comidas': comidas
        }
