import sqlite3
import pandas as pd
from datetime import datetime

def obtener_conexion():
    """Obtiene una conexión a la base de datos viajes.db"""
    conn = sqlite3.connect('viajes.db')
    conn.row_factory = sqlite3.Row
    return conn

def cargar_rendiciones_desde_excel(file_path):
    """
    Carga rendiciones desde un archivo Excel.
    Retorna: dict con success, registros_cargados, duplicados_omitidos, errores
    """
    try:
        # Leer Excel
        df = pd.read_excel(file_path, engine='openpyxl')
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        registros_cargados = 0
        duplicados_omitidos = 0
        errores = []
        
        for index, row in df.iterrows():
            try:
                nro_viaje = int(row['NRO_VIAJE']) if pd.notna(row['NRO_VIAJE']) else None
                pdt = str(row['PDT']) if pd.notna(row['PDT']) else None
                ruta = str(row['RUTA']) if pd.notna(row['RUTA']) else None
                
                if nro_viaje is None:
                    errores.append(f"Fila {index + 2}: NRO_VIAJE vacío")
                    continue
                
                # Intentar insertar (sin rendicion_valor)
                cursor.execute('''
                    INSERT INTO rendiciones (nro_viaje, pdt, ruta)
                    VALUES (?, ?, ?)
                ''', (nro_viaje, pdt, ruta))
                
                registros_cargados += 1
                
            except sqlite3.IntegrityError:
                # Viaje duplicado
                duplicados_omitidos += 1
            except Exception as e:
                errores.append(f"Fila {index + 2}: {str(e)}")
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'registros_cargados': registros_cargados,
            'duplicados_omitidos': duplicados_omitidos,
            'errores': errores
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'registros_cargados': 0,
            'duplicados_omitidos': 0,
            'errores': [str(e)]
        }

def obtener_rendiciones(filtro='activas'):
    """
    Obtiene rendiciones de la base de datos.
    filtro='activas' → Solo 'SIN REVISAR' y 'NO'
    filtro='todas' → Todas las rendiciones
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    if filtro == 'activas':
        cursor.execute('''
            SELECT 
                id, nro_viaje, pdt, ruta,
                fecha_creacion, fecha_modificacion, estado_rendicion
            FROM rendiciones
            WHERE estado_rendicion IN ('SIN REVISAR', 'NO')
            ORDER BY nro_viaje DESC
        ''')
    else:
        cursor.execute('''
            SELECT 
                id, nro_viaje, pdt, ruta,
                fecha_creacion, fecha_modificacion, estado_rendicion
            FROM rendiciones
            ORDER BY nro_viaje DESC
        ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convertir a lista de diccionarios
    rendiciones = []
    for row in rows:
        rendiciones.append({
            'id': row['id'],
            'nro_viaje': row['nro_viaje'],
            'pdt': row['pdt'],
            'ruta': row['ruta'],
            'fecha_creacion': row['fecha_creacion'],
            'fecha_modificacion': row['fecha_modificacion'],
            'estado_rendicion': row['estado_rendicion']
        })
    
    return rendiciones

def actualizar_estado_rendicion(nro_viaje, nuevo_estado):
    """
    Actualiza el estado de rendición de un viaje.
    nuevo_estado: 'SI', 'NO', o 'SIN REVISAR'
    """
    try:
        if nuevo_estado not in ['SI', 'NO', 'SIN REVISAR']:
            return {'success': False, 'error': 'Estado inválido'}
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE rendiciones
            SET estado_rendicion = ?,
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE nro_viaje = ?
        ''', (nuevo_estado, nro_viaje))
        
        if cursor.rowcount == 0:
            conn.close()
            return {'success': False, 'error': 'Viaje no encontrado'}
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': f'Estado actualizado a {nuevo_estado}'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def obtener_rendiciones_por_fecha(fecha_inicio, fecha_fin):
    """
    Obtiene rendiciones por rango de fechas (para reportes).
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            nro_viaje, pdt, ruta,
            fecha_creacion, fecha_modificacion, estado_rendicion
        FROM rendiciones
        WHERE DATE(fecha_creacion) BETWEEN ? AND ?
        ORDER BY fecha_creacion DESC
    ''', (fecha_inicio, fecha_fin))
    
    rows = cursor.fetchall()
    conn.close()
    
    rendiciones = []
    for row in rows:
        rendiciones.append({
            'nro_viaje': row['nro_viaje'],
            'pdt': row['pdt'],
            'ruta': row['ruta'],
            'fecha_creacion': row['fecha_creacion'],
            'fecha_modificacion': row['fecha_modificacion'],
            'estado_rendicion': row['estado_rendicion']
        })
    
    return rendiciones
