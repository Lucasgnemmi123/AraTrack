"""
Database Manager - Gestión de base de datos SQLite
Estructura exacta según documento: viajes + comidas_preparadas
"""
import sqlite3
import os
import sys

class DBManager:
    def __init__(self):
        # Si se ejecuta empaquetado, usar directorio del ejecutable
        # Si no, usar directorio del script
        if getattr(sys, 'frozen', False):
            # Ejecutable empaquetado: viajes.db está junto al .exe
            base_dir = os.path.dirname(sys.executable)
        else:
            # Desarrollo: viajes.db está junto a db_manager.py
            base_dir = os.path.dirname(__file__)
        
        self.db_path = os.path.join(base_dir, 'viajes.db')
    
    def get_connection(self):
        """Obtener conexión a la base de datos con configuración óptima"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=30.0,  # Mayor timeout para esperar en caso de bloqueo
            check_same_thread=False,
            isolation_level=None  # Modo autocommit para mejor concurrencia
        )
        # Habilitar WAL mode para mejor concurrencia (lecturas y escrituras simultáneas)
        conn.execute('PRAGMA journal_mode=WAL')
        # Configurar busy timeout
        conn.execute('PRAGMA busy_timeout=30000')
        return conn
    
    def init_database(self):
        """Inicializar tablas con estructura exacta del documento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Activar WAL mode para toda la base de datos
        cursor.execute('PRAGMA journal_mode=WAL')
        
        # Verificar que las tablas ya existen (fueron creadas por configurar_viajes_repetidos.py)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='viajes'")
        if cursor.fetchone() is None:
            print("Tabla viajes no existe. Ejecuta configurar_viajes_repetidos.py primero")
            conn.close()
            return
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='comidas_preparadas'")
        if cursor.fetchone() is None:
            print("Tabla comidas_preparadas no existe. Ejecuta configurar_viajes_repetidos.py primero")
            conn.close()
            return
        
        conn.close()
        print("Base de datos inicializada con soporte multi-usuario (WAL mode)")

    def insert_viaje(self, viaje_data):
        """Insertar nuevo viaje con todos los campos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Lista de todos los campos (SIN columnas de firmas - solo aparecen en PDF)
            campos = [
                'numero_viaje', 'casino', 'ruta', 'tipo_camion', 
                'patente_camion', 'patente_semi', 'numero_rampa', 'peso_camion', 
                'costo_codigo', 'termografos_gps', 'fecha', 'fecha_hora_llegada_dhl', 
                'fecha_hora_salida_dhl', 'conductor', 'celular', 'rut', 'numero_camion', 
                'num_wencos', 'bin', 'pallets', 'pallets_chep', 
                'pallets_pl_negro_grueso', 'pallets_pl_negro_alternativo',
                'pallets_refrigerado', 'wencos_refrigerado', 'pallets_congelado', 'wencos_congelado', 
                'pallets_abarrote',
                'check_congelado', 'check_refrigerado', 'check_abarrote', 
                'check_implementos', 'check_aseo', 'check_trazabilidad', 'check_plataforma_wtck', 
                'check_env_correo_wtck', 'check_revision_planilla_despacho', 'sello_salida_1p', 
                'sello_salida_2p', 'sello_salida_3p', 'sello_salida_4p', 'sello_salida_5p', 
                'sello_retorno_1p', 'sello_retorno_2p', 'sello_retorno_3p', 'sello_retorno_4p', 
                'sello_retorno_5p', 'guia_1', 'guia_2', 'guia_3', 'guia_4', 'guia_5', 'guia_6', 
                'guia_7', 'guia_8', 'guia_9', 'guia_10', 'guia_11', 'guia_12', 'guia_13', 'guia_14',
                'guia_15', 'guia_16', 'guia_17', 'guia_18', 'guia_19', 'guia_20', 'guia_21',
                'numero_certificado_fumigacion', 'revision_limpieza_camion_acciones', 
                'administrativo_responsable'
            ]
            
            # Preparar valores con defaults
            valores = []
            for campo in campos:
                valores.append(viaje_data.get(campo, ''))
            
            # Crear query dinámico
            placeholders = ', '.join(['?' for _ in campos])
            query = f'''
                INSERT INTO viajes ({', '.join(campos)})
                VALUES ({placeholders})
            '''
            
            cursor.execute(query, valores)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error insertando viaje: {e}")
            return False
    
    def insert_viaje_por_centro(self, viaje_data, centro_costo):
        """Insertar viaje específico para un centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar si ya existe este viaje para este centro de costo
            cursor.execute('''
                SELECT COUNT(*) FROM viajes v
                JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje
                WHERE v.numero_viaje = ? AND c.numero_centro_costo = ?
            ''', (viaje_data.get('numero_viaje'), centro_costo))
            
            existe = cursor.fetchone()[0] > 0
            
            if not existe:
                # Lista de todos los campos (SIN columnas de firmas - solo aparecen en PDF)
                campos = [
                    'numero_viaje', 'casino', 'ruta', 'tipo_camion', 
                    'patente_camion', 'patente_semi', 'numero_rampa', 'peso_camion', 
                    'costo_codigo', 'termografos_gps', 'fecha', 'fecha_hora_llegada_dhl', 
                    'fecha_hora_salida_dhl', 'conductor', 'celular', 'rut', 'numero_camion', 
                    'num_wencos', 'bin', 'pallets', 'pallets_chep', 
                    'pallets_pl_negro_grueso', 'pallets_pl_negro_alternativo',
                    'pallets_refrigerado', 'wencos_refrigerado', 'pallets_congelado', 'wencos_congelado', 
                    'pallets_abarrote',
                    'check_congelado', 'check_refrigerado', 'check_abarrote', 
                    'check_implementos', 'check_aseo', 'check_trazabilidad', 'check_plataforma_wtck', 
                    'check_env_correo_wtck', 'check_revision_planilla_despacho', 'sello_salida_1p', 
                    'sello_salida_2p', 'sello_salida_3p', 'sello_salida_4p', 'sello_salida_5p', 
                    'sello_retorno_1p', 'sello_retorno_2p', 'sello_retorno_3p', 'sello_retorno_4p', 
                    'sello_retorno_5p', 'guia_1', 'guia_2', 'guia_3', 'guia_4', 'guia_5', 'guia_6', 
                    'guia_7', 'guia_8', 'guia_9', 'guia_10', 'guia_11', 'guia_12', 'guia_13', 'guia_14',
                    'guia_15', 'guia_16', 'guia_17', 'guia_18', 'guia_19', 'guia_20', 'guia_21',
                    'numero_certificado_fumigacion', 'revision_limpieza_camion_acciones', 
                    'administrativo_responsable'
                ]
                
                # Preparar valores con defaults
                valores = []
                for campo in campos:
                    valores.append(viaje_data.get(campo, ''))
                
                # Crear query dinámico
                placeholders = ', '.join(['?' for _ in campos])
                query = f'''
                    INSERT INTO viajes ({', '.join(campos)})
                    VALUES ({placeholders})
                '''
                
                cursor.execute(query, valores)
                viaje_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return viaje_id
            else:
                conn.close()
                return True  # Ya existe, no es error
                
        except Exception as e:
            print(f"Error insertando viaje por centro: {e}")
            return False
    
    def insert_comida(self, comida_data):
        """Insertar comida preparada"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO comidas_preparadas 
                (numero_viaje, guia_comida, descripcion, kilo, bultos, numero_centro_costo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                comida_data.get('numero_viaje'),
                comida_data.get('guia_comida', ''),
                comida_data.get('descripcion', ''),
                comida_data.get('kilo', ''),
                comida_data.get('bultos', ''),
                comida_data.get('numero_centro_costo', '32062')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error insertando comida: {e}")
            return False
    
    def get_viaje(self, numero_viaje):
        """Obtener viaje por número"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM viajes WHERE numero_viaje = ?', (numero_viaje,))
            viaje = cursor.fetchone()
            
            conn.close()
            return viaje
        except Exception as e:
            print(f"Error obteniendo viaje: {e}")
            return None
    
    def get_comidas_por_viaje(self, numero_viaje):
        """Obtener comidas por viaje agrupadas por centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM comidas_preparadas 
                WHERE numero_viaje = ? 
                ORDER BY numero_centro_costo, id
            ''', (numero_viaje,))
            
            comidas = cursor.fetchall()
            conn.close()
            return comidas
        except Exception as e:
            print(f"Error obteniendo comidas: {e}")
            return []

    def update_viaje(self, numero_viaje, viaje_data):
        """Actualizar viaje existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE viajes 
                SET casino = ?, conductor = ?, fecha = ?
                WHERE numero_viaje = ?
            ''', (
                viaje_data.get('casino', ''),
                viaje_data.get('conductor', ''),
                viaje_data.get('fecha', ''),
                numero_viaje
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error actualizando viaje: {e}")
            return False
    
    def delete_viaje(self, viaje_id):
        """Eliminar viaje por ID y sus comidas asociadas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            print(f"[DELETE_VIAJE] Eliminando viaje con ID: {viaje_id}")
            
            # Primero obtener numero_viaje para eliminar comidas
            cursor.execute('SELECT numero_viaje FROM viajes WHERE id = ?', (viaje_id,))
            result = cursor.fetchone()
            
            if result:
                numero_viaje = result[0]
                print(f"[DELETE_VIAJE] Numero de viaje encontrado: {numero_viaje}")
                
                # Eliminar comidas asociadas
                cursor.execute('DELETE FROM comidas_preparadas WHERE numero_viaje = ?', (numero_viaje,))
                comidas_deleted = cursor.rowcount
                print(f"[DELETE_VIAJE] Comidas eliminadas: {comidas_deleted}")
                
                # Eliminar el viaje
                cursor.execute('DELETE FROM viajes WHERE id = ?', (viaje_id,))
                viajes_deleted = cursor.rowcount
                print(f"[DELETE_VIAJE] Viajes eliminados: {viajes_deleted}")
            else:
                print(f"[DELETE_VIAJE] ERROR: No se encontró viaje con ID {viaje_id}")
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error eliminando viaje: {e}")
            return False
    
    def delete_comida(self, comida_id):
        """Eliminar comida específica"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM comidas_preparadas WHERE id = ?', (comida_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error eliminando comida: {e}")
            return False
    
    def buscar_viajes_avanzado(self, filtros):
        """Búsqueda avanzada con múltiples filtros"""
        try:
            conn = self.get_connection()
            
            # Construir query dinámico
            where_clauses = []
            params = []
            
            if filtros.get('numero_viaje'):
                where_clauses.append("v.numero_viaje LIKE ?")
                params.append(f"%{filtros['numero_viaje']}%")
            
            if filtros.get('conductor'):
                where_clauses.append("v.conductor LIKE ?")
                params.append(f"%{filtros['conductor']}%")
            
            if filtros.get('casino'):
                where_clauses.append("v.casino LIKE ?")
                params.append(f"%{filtros['casino']}%")
                
            if filtros.get('fecha_desde'):
                where_clauses.append("v.fecha >= ?")
                params.append(filtros['fecha_desde'])
                
            if filtros.get('fecha_hasta'):
                where_clauses.append("v.fecha <= ?")
                params.append(filtros['fecha_hasta'])
            
            where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
            
            query = f"""
                SELECT v.numero_viaje, v.casino, v.conductor, v.fecha, 
                       COUNT(c.id) as total_comidas, v.observaciones
                FROM viajes v
                LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje
                {where_sql}
                GROUP BY v.id
                ORDER BY v.created_at DESC
            """
            
            cursor = conn.cursor()
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()
            return resultados
        except Exception as e:
            print(f"Error en búsqueda avanzada: {e}")
            return []
    
    def buscar_viajes_avanzado(self, filtros):
        """Búsqueda avanzada de viajes con múltiples criterios"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT v.numero_viaje, v.casino, v.conductor, v.fecha, 
                       COUNT(c.id) as total_comidas, v.observaciones
                FROM viajes v
                LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje
                WHERE 1=1
            """
            params = []
            
            # Filtros opcionales
            if filtros.get('numero_viaje'):
                query += " AND v.numero_viaje LIKE ?"
                params.append(f"%{filtros['numero_viaje']}%")
            
            if filtros.get('conductor'):
                query += " AND v.conductor LIKE ?"
                params.append(f"%{filtros['conductor']}%")
            
            if filtros.get('casino'):
                query += " AND v.casino LIKE ?"
                params.append(f"%{filtros['casino']}%")
            
            if filtros.get('fecha_desde'):
                query += " AND v.fecha >= ?"
                params.append(filtros['fecha_desde'])
            
            if filtros.get('fecha_hasta'):
                query += " AND v.fecha <= ?"
                params.append(filtros['fecha_hasta'])
            
        except Exception as e:
            print(f"Error en búsqueda avanzada: {e}")
            return []

    # === MÉTODOS ESPECÍFICOS PARA VIAJES REPETIDOS CON DIFERENTES CÓDIGOS DE COSTO ===
    
    def get_viajes_por_numero(self, numero_viaje):
        """Obtener TODOS los registros de un mismo número de viaje (diferentes centros de costo)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT v.*, 
                       COUNT(c.id) as total_comidas
                FROM viajes v
                LEFT JOIN comidas_preparadas c ON v.numero_viaje = c.numero_viaje 
                                                  AND v.costo_codigo = c.numero_centro_costo
                WHERE v.numero_viaje = ?
                GROUP BY v.id
                ORDER BY v.costo_codigo
            ''', (numero_viaje,))
            
            viajes = cursor.fetchall()
            conn.close()
            return viajes
        except Exception as e:
            print(f"Error obteniendo viajes por número: {e}")
            return []
    
    def get_viaje_por_numero_y_centro(self, numero_viaje, codigo_centro):
        """Obtener un viaje específico por número y centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM viajes 
                WHERE numero_viaje = ? AND costo_codigo = ?
            ''', (numero_viaje, codigo_centro))
            
            viaje_tuple = cursor.fetchone()
            
            if viaje_tuple:
                # Convertir tupla a diccionario
                column_names = [description[0] for description in cursor.description]
                viaje = dict(zip(column_names, viaje_tuple))
                conn.close()
                return viaje
            
            conn.close()
            return None
        except Exception as e:
            print(f"Error obteniendo viaje específico: {e}")
            return None
    
    def get_comidas_por_viaje_y_centro(self, numero_viaje, codigo_centro):
        """Obtener comidas de un viaje para un centro de costo específico"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM comidas_preparadas 
                WHERE numero_viaje = ? AND numero_centro_costo = ?
                ORDER BY id
            ''', (numero_viaje, codigo_centro))
            
            comidas_tuplas = cursor.fetchall()
            
            # Convertir tuplas a diccionarios
            comidas = []
            if comidas_tuplas:
                column_names = [description[0] for description in cursor.description]
                for tupla in comidas_tuplas:
                    comidas.append(dict(zip(column_names, tupla)))
            
            conn.close()
            return comidas
        except Exception as e:
            print(f"Error obteniendo comidas por viaje y centro: {e}")
            return []
    
    def get_centros_costo_por_viaje(self, numero_viaje):
        """Obtener todos los centros de costo de un número de viaje"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT costo_codigo 
                FROM viajes 
                WHERE numero_viaje = ?
                ORDER BY costo_codigo
            ''', (numero_viaje,))
            
            centros = [row[0] for row in cursor.fetchall()]
            conn.close()
            return centros
        except Exception as e:
            print(f"Error obteniendo centros de costo: {e}")
            return []
    
    def get_ultimo_registro_viaje(self, numero_viaje):
        """Obtener el último registro de un número de viaje específico"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener el registro más reciente por ID (asumiendo que ID es autoincremental)
            cursor.execute('''
                SELECT * FROM viajes 
                WHERE numero_viaje = ? 
                ORDER BY id DESC 
                LIMIT 1
            ''', (numero_viaje,))
            
            row = cursor.fetchone()
            if row:
                # Obtener nombres de columnas
                cursor.execute("PRAGMA table_info(viajes)")
                columns = [col[1] for col in cursor.fetchall()]
                
                # Crear diccionario con los datos
                viaje_data = dict(zip(columns, row))
                conn.close()
                return viaje_data
            else:
                conn.close()
                return None
        except Exception as e:
            print(f"Error obteniendo último registro: {e}")
            return None
    
    def exists_viaje_centro(self, numero_viaje, codigo_centro):
        """Verificar si ya existe un viaje con ese número y centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM viajes 
                WHERE numero_viaje = ? AND costo_codigo = ?
            ''', (numero_viaje, codigo_centro))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except Exception as e:
            print(f"Error verificando existencia: {e}")
            return False
    
    def insert_comida_con_centro(self, comida_data):
        """Insertar comida asociada a viaje y centro de costo específico"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO comidas_preparadas 
                (numero_viaje, numero_centro_costo, guia_comida, descripcion, kilo, bultos)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                comida_data.get('numero_viaje'),
                comida_data.get('numero_centro_costo'),
                comida_data.get('guia_comida', ''),
                comida_data.get('descripcion', ''),
                comida_data.get('kilo', ''),
                comida_data.get('bultos', '')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error insertando comida con centro: {e}")
            return False
    
    def get_estadisticas_viajes_repetidos(self):
        """Obtener estadísticas de viajes repetidos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total viajes únicos vs total registros
            cursor.execute('SELECT COUNT(DISTINCT numero_viaje) FROM viajes')
            viajes_unicos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM viajes')
            total_registros = cursor.fetchone()[0]
            
            # Viajes con múltiples centros de costo
            cursor.execute('''
                SELECT numero_viaje, COUNT(DISTINCT costo_codigo) as centros
                FROM viajes 
                GROUP BY numero_viaje 
                HAVING COUNT(DISTINCT costo_codigo) > 1
            ''')
            viajes_multiples = cursor.fetchall()
            
            conn.close()
            
            return {
                'viajes_unicos': viajes_unicos,
                'total_registros': total_registros,
                'viajes_multiples': viajes_multiples
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def update_viaje_by_numero_centro(self, numero_viaje_original, centro_costo_original, viaje_data):
        """Actualizar un viaje específico por número de viaje y centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Lista de campos actualizables (EXCLUIR numero_viaje y costo_codigo que son la clave)
            campos = [
                'casino', 'ruta', 'tipo_camion', 
                'patente_camion', 'patente_semi', 'numero_rampa', 'peso_camion', 
                'termografos_gps', 'fecha', 'fecha_hora_llegada_dhl', 
                'fecha_hora_salida_dhl', 'conductor', 'celular', 'rut', 'numero_camion', 
                'num_wencos', 'bin', 'pallets', 'pallets_chep', 'pallets_refrigerado', 
                'wencos_refrigerado', 'pallets_congelado', 'wencos_congelado', 
                'pallets_abarrote', 'check_congelado', 'check_refrigerado', 'check_abarrote', 
                'check_implementos', 'check_aseo', 'check_trazabilidad', 'check_plataforma_wtck', 
                'check_env_correo_wtck', 'check_revision_planilla_despacho', 'sello_salida_1p', 
                'sello_salida_2p', 'sello_salida_3p', 'sello_salida_4p', 'sello_salida_5p', 
                'sello_retorno_1p', 'sello_retorno_2p', 'sello_retorno_3p', 'sello_retorno_4p', 
                'sello_retorno_5p', 'guia_1', 'guia_2', 'guia_3', 'guia_4', 'guia_5', 'guia_6', 
                'guia_7', 'guia_8', 'guia_9', 'guia_10', 'guia_11', 'guia_12', 'guia_13', 'guia_14',
                'guia_15', 'guia_16', 'guia_17', 'guia_18', 'guia_19', 'guia_20', 'guia_21',
                'numero_certificado_fumigacion', 'revision_limpieza_camion_acciones', 
                'administrativo_responsable'
            ]
            
            # Crear SET clause
            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            
            # Preparar valores
            valores = []
            for campo in campos:
                valores.append(viaje_data.get(campo, ''))
            
            # Agregar condiciones WHERE al final
            valores.extend([numero_viaje_original, centro_costo_original])
            
            # Ejecutar UPDATE
            query = f"UPDATE viajes SET {set_clause} WHERE numero_viaje = ? AND costo_codigo = ?"
            cursor.execute(query, valores)
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error actualizando viaje: {e}")
            return False
    
    def delete_comidas_by_viaje_centro(self, numero_viaje, centro_costo):
        """Eliminar todas las comidas de un viaje específico por centro de costo"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM comidas_preparadas 
                WHERE numero_viaje = ? AND numero_centro_costo = ?
            ''', (numero_viaje, centro_costo))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error eliminando comidas: {e}")
            return False
    
    def get_centros_costo_por_viaje(self, numero_viaje):
        """Obtener lista de centros de costo existentes para un número de viaje"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT costo_codigo FROM viajes 
                WHERE numero_viaje = ?
                ORDER BY costo_codigo
            ''', (numero_viaje,))
            
            centros = [row[0] for row in cursor.fetchall()]
            conn.close()
            return centros
        except Exception as e:
            print(f"Error obteniendo centros de costo: {e}")
            return []
