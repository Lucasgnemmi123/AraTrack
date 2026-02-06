from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from datetime import datetime
import os
from db_manager import DBManager
from maestras_manager import MaestrasManager
from pdf_generator import PDFGenerator
from auth_manager import AuthManager, login_required

app = Flask(__name__)
app.secret_key = 'aratrack-pro-2025-secure-key'
db_manager = DBManager()
maestras_manager = MaestrasManager()
pdf_generator = PDFGenerator()
auth_manager = AuthManager()

# ========== RUTAS DE AUTENTICACIÓN ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = auth_manager.verify_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nombre_completo'] = user['nombre_completo']
            flash(f'Bienvenido, {user["nombre_completo"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('login'))

# ========== GESTIÓN DE USUARIOS (SOLO ADMIN) ==========

@app.route('/gestionar-usuarios')
@login_required
def gestionar_usuarios():
    # Solo admin puede acceder
    if session.get('username') != 'admin':
        flash('No tienes permisos para acceder a esta sección', 'error')
        return redirect(url_for('index'))
    return render_template('gestionar_usuarios.html')

@app.route('/api/usuarios')
@login_required
def api_listar_usuarios():
    if session.get('username') != 'admin':
        return jsonify({'success': False, 'message': 'Sin permisos'}), 403
    
    usuarios = auth_manager.get_all_users()
    return jsonify({'success': True, 'usuarios': usuarios})

@app.route('/api/crear-usuario', methods=['POST'])
@login_required
def api_crear_usuario():
    if session.get('username') != 'admin':
        return jsonify({'success': False, 'message': 'Sin permisos'}), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    nombre_completo = data.get('nombre_completo')
    email = data.get('email')
    
    # Crear usuario con la contraseña proporcionada
    success, result = auth_manager.create_user(username, password, nombre_completo, email)
    
    if success:
        return jsonify({'success': True, 'message': 'Usuario creado exitosamente', 'user_id': result})
    else:
        return jsonify({'success': False, 'message': result})

@app.route('/api/cambiar-password', methods=['POST'])
@login_required
def api_cambiar_password():
    if session.get('username') != 'admin':
        return jsonify({'success': False, 'message': 'Sin permisos'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    nueva_password = data.get('nueva_password')
    
    if not nueva_password or len(nueva_password) < 4:
        return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 4 caracteres'})
    
    success, message = auth_manager.change_user_password(user_id, nueva_password)
    
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/api/toggle-usuario', methods=['POST'])
@login_required
def api_toggle_usuario():
    if session.get('username') != 'admin':
        return jsonify({'success': False, 'message': 'Sin permisos'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    success = auth_manager.toggle_user_status(user_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Estado actualizado'})
    else:
        return jsonify({'success': False, 'message': 'Error al actualizar'})

@app.route('/api/eliminar-usuario', methods=['POST'])
@login_required
def api_eliminar_usuario():
    if session.get('username') != 'admin':
        return jsonify({'success': False, 'message': 'Sin permisos'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    success, message = auth_manager.delete_user(user_id)
    
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message})

# ========== RUTAS PRINCIPALES (PROTEGIDAS) ==========

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/nuevo-viaje')
@login_required
def nuevo_viaje():
    casinos = maestras_manager.obtener_todos_casinos()
    choferes_data = maestras_manager.obtener_todos_los_choferes()
    choferes = [c['nombre'] for c in choferes_data]
    centros_costo = maestras_manager.obtener_todos_centros_costo()
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT patente_camion FROM viajes WHERE patente_camion IS NOT NULL ORDER BY patente_camion')
    patentes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return render_template('nuevo_viaje.html', casinos=casinos, choferes=choferes, patentes=patentes, centros_costo=centros_costo)

@app.route('/api/buscar-centros-costo/<numero_viaje>')
def buscar_centros_costo(numero_viaje):
    """Devuelve lista de centros con su información de casino"""
    centros_codigos = db_manager.get_centros_costo_por_viaje(numero_viaje)
    centros_info = []
    
    for codigo in centros_codigos:
        casino_data = maestras_manager.buscar_casino_por_codigo(int(codigo))
        centros_info.append({
            'codigo': codigo,
            'casino': casino_data['casino'] if casino_data else 'Sin casino',
            'ruta': casino_data['ruta'] if casino_data else ''
        })
    
    return jsonify(centros_info)

@app.route('/api/obtener-centros-costo')
def obtener_centros_costo():
    """Endpoint para obtener todos los centros de costo"""
    centros = maestras_manager.obtener_todos_centros_costo()
    return jsonify(centros)

@app.route('/api/centro-costo-detalles/<int:codigo>')
def centro_costo_detalles(codigo):
    """Endpoint que retorna casino y ruta para un código de centro de costo"""
    try:
        centro = maestras_manager.buscar_casino_por_codigo(codigo)
        if centro:
            return jsonify({
                'success': True,
                'casino': centro['casino'],
                'ruta': centro['ruta']
            })
        else:
            return jsonify({'success': False, 'message': 'Centro de costo no encontrado'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/obtener-choferes-completo')
def obtener_choferes_completo():
    choferes = maestras_manager.obtener_todos_los_choferes()
    return jsonify(choferes)

@app.route('/test-cargar')
def test_cargar():
    return render_template('test_cargar.html')

@app.route('/api/buscar-viaje-numero/<numero_viaje>')
def buscar_viaje_numero(numero_viaje):
    try:
        print(f"\nBUSCANDO VIAJE: {numero_viaje}")
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM viajes 
            WHERE numero_viaje = ? 
            ORDER BY id DESC LIMIT 1
        """, (numero_viaje,))
        
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            viaje = dict(zip(columns, row))
            
            # Obtener comidas del viaje
            cursor.execute('''
                SELECT id, numero_viaje, numero_centro_costo, guia_comida, 
                       descripcion, kilo, bultos 
                FROM comidas_preparadas 
                WHERE numero_viaje = ? AND numero_centro_costo = ?
                ORDER BY id
            ''', (numero_viaje, viaje.get('costo_codigo')))
            
            comidas_rows = cursor.fetchall()
            comidas = []
            for row in comidas_rows:
                comidas.append({
                    'id': row[0],
                    'numero_viaje': row[1],
                    'numero_centro_costo': row[2],
                    'guia_comida': row[3],
                    'descripcion': row[4],
                    'kilo': row[5],
                    'bultos': row[6]
                })
            
            conn.close()
            
            print(f"VIAJE ENCONTRADO:")
            print(f"   - Conductor: {viaje.get('conductor')}")
            print(f"   - Centro Costo: {viaje.get('costo_codigo')}")
            print(f"   - Salida: {viaje.get('fecha_hora_salida_dhl')}")
            print(f"   - Llegada: {viaje.get('fecha_hora_llegada_dhl')}")
            print(f"   - Celular: {viaje.get('celular')}")
            print(f"   - RUT: {viaje.get('rut')}")
            print(f"   - Comidas: {len(comidas)}")
            return jsonify({'success': True, 'viaje': viaje, 'comidas': comidas})
        else:
            conn.close()
            print(f"VIAJE NO ENCONTRADO")
            return jsonify({'success': False})
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/casino-por-centro/<centro_costo>')
def casino_por_centro(centro_costo):
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT codigo, nombre, ruta 
            FROM casinos 
            WHERE centro_costo = ?
            LIMIT 1
        """, (centro_costo,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            casino = {
                'codigo': row[0],
                'nombre': row[1],
                'ruta': row[2]
            }
            return jsonify({'success': True, 'casino': casino})
        else:
            return jsonify({'success': False})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/actualizar-casino', methods=['POST'])
def actualizar_casino():
    try:
        data = request.json
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE casinos 
            SET nombre = ?, ruta = ?
            WHERE codigo = ?
        """, (data.get('nombre'), data.get('ruta'), data.get('codigo')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/actualizar-conductor', methods=['POST'])
def actualizar_conductor():
    try:
        data = request.json
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE choferes 
            SET celular = ?, rut = ?
            WHERE nombre = ?
        """, (data.get('celular'), data.get('rut'), data.get('nombre')))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/guardar-viaje', methods=['POST'])
def guardar_viaje():
    try:
        data = request.json
        
        # Preparar datos del viaje
        viaje_data = {
            'numero_viaje': data.get('numero_viaje'),
            'costo_codigo': data.get('centro_costo'),
            'fecha': data.get('fecha'),
            'casino': data.get('codigo_casino', ''),
            'ruta': data.get('ruta', ''),
            'tipo_camion': data.get('tipo_camion', ''),
            'patente_camion': data.get('patente_camion'),
            'patente_semi': data.get('patente_semi', ''),
            'numero_rampa': data.get('numero_rampa', ''),
            'peso_camion': data.get('peso_camion', ''),
            'numero_camion': data.get('numero_camion', ''),
            'termografos_gps': data.get('termografos_gps', ''),
            'conductor': data.get('chofer'),
            'celular': data.get('celular', ''),
            'rut': data.get('rut', ''),
            'fecha_hora_salida_dhl': data.get('hora_salida', ''),
            'fecha_hora_llegada_dhl': data.get('hora_llegada', ''),
            'num_wencos': data.get('num_wencos', ''),
            'bin': data.get('bin', ''),
            'pallets': data.get('pallets', ''),
            'pallets_chep': data.get('pallets_chep', ''),
            'pallets_pl_negro_grueso': data.get('pallets_pl_negro_grueso', ''),
            'pallets_pl_negro_alternativo': data.get('pallets_pl_negro_alternativo', ''),
            'pallets_congelado': data.get('pallets_congelado', ''),
            'wencos_congelado': data.get('wencos_congelado', ''),
            'check_congelado': data.get('check_congelado', ''),
            'pallets_refrigerado': data.get('pallets_refrigerado', ''),
            'wencos_refrigerado': data.get('wencos_refrigerado', ''),
            'check_refrigerado': data.get('check_refrigerado', ''),
            'pallets_abarrote': data.get('pallets_abarrote', ''),

            'check_abarrote': data.get('check_abarrote', ''),
            'check_implementos': data.get('check_implementos', ''),
            'check_aseo': data.get('check_aseo', ''),
            'check_trazabilidad': data.get('check_trazabilidad', ''),
            'check_plataforma_wtck': data.get('check_plataforma_wtck', ''),
            'check_env_correo_wtck': data.get('check_env_correo_wtck', ''),
            'check_revision_planilla_despacho': data.get('check_revision_planilla_despacho', ''),
            'guia_1': data.get('guia_1', ''),
            'guia_2': data.get('guia_2', ''),
            'guia_3': data.get('guia_3', ''),
            'guia_4': data.get('guia_4', ''),
            'guia_5': data.get('guia_5', ''),
            'guia_6': data.get('guia_6', ''),
            'guia_7': data.get('guia_7', ''),
            'guia_8': data.get('guia_8', ''),
            'guia_9': data.get('guia_9', ''),
            'guia_10': data.get('guia_10', ''),
            'guia_11': data.get('guia_11', ''),
            'guia_12': data.get('guia_12', ''),
            'guia_13': data.get('guia_13', ''),
            'guia_14': data.get('guia_14', ''),
            'sello_salida_1p': data.get('sello_salida_1p', ''),
            'sello_salida_2p': data.get('sello_salida_2p', ''),
            'sello_salida_3p': data.get('sello_salida_3p', ''),
            'sello_salida_4p': data.get('sello_salida_4p', ''),
            'sello_salida_5p': data.get('sello_salida_5p', ''),
            'sello_retorno_1p': data.get('sello_retorno_1p', ''),
            'sello_retorno_2p': data.get('sello_retorno_2p', ''),
            'sello_retorno_3p': data.get('sello_retorno_3p', ''),
            'sello_retorno_4p': data.get('sello_retorno_4p', ''),
            'sello_retorno_5p': data.get('sello_retorno_5p', ''),
            'numero_certificado_fumigacion': data.get('numero_certificado_fumigacion', ''),
            'revision_limpieza_camion_acciones': data.get('revision_limpieza_camion_acciones', ''),
            'administrativo_responsable': data.get('administrativo_responsable', '')
        }
        
        # Insertar viaje
        result = db_manager.insert_viaje(viaje_data)
        
        if result:
            # Insertar comidas preparadas con el centro de costo del viaje
            comidas = data.get('comidas', [])
            if comidas:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                for comida in comidas:
                    cursor.execute("""
                        INSERT INTO comidas_preparadas (
                            numero_viaje, numero_centro_costo, guia_comida, 
                            descripcion, kilo, bultos
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        data.get('numero_viaje'),
                        data.get('centro_costo'),
                        comida.get('guia_comida', ''),
                        comida.get('descripcion'),
                        comida.get('kilo', 0),
                        comida.get('bultos', 0)
                    ))
                
                conn.commit()
                conn.close()
            
            mensaje = f'Viaje {data.get("numero_viaje")} creado exitosamente'
            if comidas:
                mensaje += f' con {len(comidas)} comida(s) preparada(s)'
            
            return jsonify({'success': True, 'message': mensaje})
        else:
            return jsonify({'success': False, 'message': 'Error al guardar el viaje'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/editar-viaje')
@login_required
def editar_viaje():
    return render_template('editar_viaje.html')

@app.route('/api/buscar-viaje', methods=['POST'])
def buscar_viaje():
    try:
        data = request.json
        numero_viaje = data.get('numero_viaje')
        centro_costo = data.get('centro_costo')
        
        # Obtener viaje
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM viajes WHERE numero_viaje = ? AND costo_codigo = ?', 
                      (numero_viaje, centro_costo))
        viaje_row = cursor.fetchone()
        
        if not viaje_row:
            conn.close()
            return jsonify({'success': False, 'message': 'Viaje no encontrado'}), 404
        
        # Convertir a diccionario
        columns = [description[0] for description in cursor.description]
        viaje = dict(zip(columns, viaje_row))
        
        # Obtener comidas
        cursor.execute('''
            SELECT id, numero_viaje, numero_centro_costo, guia_comida, 
                   descripcion, kilo, bultos 
            FROM comidas_preparadas 
            WHERE numero_viaje = ? AND numero_centro_costo = ?
            ORDER BY id
        ''', (numero_viaje, centro_costo))
        
        comidas_rows = cursor.fetchall()
        comidas = []
        for row in comidas_rows:
            comidas.append({
                'id': row[0],
                'numero_viaje': row[1],
                'numero_centro_costo': row[2],
                'guia_comida': row[3],
                'descripcion': row[4],
                'kilo': row[5],
                'bultos': row[6]
            })
        
        conn.close()
        
        return jsonify({
            'success': True, 
            'viaje': viaje, 
            'comidas': comidas
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/actualizar-viaje', methods=['POST'])
def actualizar_viaje():
    try:
        data = request.json
        viaje_data = {
            'fecha': data.get('fecha'),
            'casino': data.get('casino'),
            'ruta': data.get('ruta'),
            'tipo_camion': data.get('tipo_camion'),
            'patente_camion': data.get('patente_camion'),
            'patente_semi': data.get('patente_semi'),
            'numero_rampa': data.get('numero_rampa'),
            'peso_camion': data.get('peso_camion'),
            'numero_camion': data.get('numero_camion'),
            'termografos_gps': data.get('termografos_gps'),
            'conductor': data.get('chofer'),
            'celular': data.get('celular'),
            'rut': data.get('rut'),
            'fecha_hora_salida_dhl': data.get('hora_salida'),
            'fecha_hora_llegada_dhl': data.get('hora_llegada'),
            'num_wencos': data.get('num_wencos'),
            'bin': data.get('bin'),
            'pallets': data.get('pallets'),
            'pallets_chep': data.get('pallets_chep'),
            'pallets_pl_negro_grueso': data.get('pallets_pl_negro_grueso', ''),
            'pallets_pl_negro_alternativo': data.get('pallets_pl_negro_alternativo', ''),
            'pallets_congelado': data.get('pallets_congelado'),
            'wencos_congelado': data.get('wencos_congelado'),
            'check_congelado': data.get('check_congelado', ''),
            'pallets_refrigerado': data.get('pallets_refrigerado'),
            'wencos_refrigerado': data.get('wencos_refrigerado'),
            'check_refrigerado': data.get('check_refrigerado', ''),
            'pallets_abarrote': data.get('pallets_abarrote'),

            'check_abarrote': data.get('check_abarrote', ''),
            'check_implementos': data.get('check_implementos', ''),
            'check_aseo': data.get('check_aseo', ''),
            'check_trazabilidad': data.get('check_trazabilidad', ''),
            'check_plataforma_wtck': data.get('check_plataforma_wtck', ''),
            'check_env_correo_wtck': data.get('check_env_correo_wtck', ''),
            'check_revision_planilla_despacho': data.get('check_revision_planilla_despacho', ''),
            'guia_1': data.get('guia_1', ''),
            'guia_2': data.get('guia_2', ''),
            'guia_3': data.get('guia_3', ''),
            'guia_4': data.get('guia_4', ''),
            'guia_5': data.get('guia_5', ''),
            'guia_6': data.get('guia_6', ''),
            'guia_7': data.get('guia_7', ''),
            'guia_8': data.get('guia_8', ''),
            'guia_9': data.get('guia_9', ''),
            'guia_10': data.get('guia_10', ''),
            'guia_11': data.get('guia_11', ''),
            'guia_12': data.get('guia_12', ''),
            'guia_13': data.get('guia_13', ''),
            'guia_14': data.get('guia_14', ''),
            'sello_salida_1p': data.get('sello_salida_1p', ''),
            'sello_salida_2p': data.get('sello_salida_2p', ''),
            'sello_salida_3p': data.get('sello_salida_3p', ''),
            'sello_salida_4p': data.get('sello_salida_4p', ''),
            'sello_salida_5p': data.get('sello_salida_5p', ''),
            'sello_retorno_1p': data.get('sello_retorno_1p', ''),
            'sello_retorno_2p': data.get('sello_retorno_2p', ''),
            'sello_retorno_3p': data.get('sello_retorno_3p', ''),
            'sello_retorno_4p': data.get('sello_retorno_4p', ''),
            'sello_retorno_5p': data.get('sello_retorno_5p', ''),
            'numero_certificado_fumigacion': data.get('numero_certificado_fumigacion', ''),
            'revision_limpieza_camion_acciones': data.get('revision_limpieza_camion_acciones', ''),
            'administrativo_responsable': data.get('administrativo_responsable', '')
        }
        
        # Actualizar viaje
        db_manager.update_viaje_by_numero_centro(data.get('numero_viaje'), data.get('centro_costo'), viaje_data)
        
        # Actualizar comidas - eliminar las existentes e insertar las nuevas
        db_manager.delete_comidas_by_viaje_centro(data.get('numero_viaje'), data.get('centro_costo'))
        
        comidas = data.get('comidas', [])
        if comidas:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            
            for comida in comidas:
                cursor.execute("""
                    INSERT INTO comidas_preparadas (
                        numero_viaje, numero_centro_costo, guia_comida, 
                        descripcion, kilo, bultos
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    data.get('numero_viaje'),
                    data.get('centro_costo'),
                    comida.get('guia_comida', ''),
                    comida.get('descripcion'),
                    comida.get('kilo', 0),
                    comida.get('bultos', 0)
                ))
            
            conn.commit()
            conn.close()
        
        return jsonify({'success': True, 'message': 'Viaje actualizado correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/eliminar-viaje', methods=['POST'])
def eliminar_viaje():
    try:
        data = request.json
        db_manager.delete_comidas_by_viaje_centro(data.get('numero_viaje'), data.get('centro_costo'))
        viaje = db_manager.get_viaje_por_numero_y_centro(data.get('numero_viaje'), data.get('centro_costo'))
        if viaje:
            db_manager.delete_viaje(viaje['id'])
            return jsonify({'success': True})
        return jsonify({'success': False}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/generar-pdf')
@login_required
def generar_pdf_page():
    return render_template('generar_pdf.html')

@app.route('/api/generar-pdf', methods=['POST'])
def generar_pdf_api():
    try:
        numero_viaje = request.json.get('numero_viaje')
        
        # Obtener todos los centros de costo del viaje
        centros = db_manager.get_centros_costo_por_viaje(numero_viaje)
        if not centros:
            return jsonify({'success': False, 'message': 'No se encontraron centros de costo para este viaje'}), 404
        
        # Generar PDF completo usando la nueva función
        pdf_path = pdf_generator.generar_pdf_completo(numero_viaje)
        
        if pdf_path and os.path.exists(pdf_path):
            num_centros = len(centros)
            return jsonify({
                'success': True, 
                'pdf_filename': os.path.basename(pdf_path),
                'message': f'PDF generado con {num_centros} hoja(s) - una por centro de costo'
            })
        return jsonify({'success': False, 'message': 'Error al generar el PDF'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/descargar-pdf/<path:filename>')
def descargar_pdf(filename):
    filepath = os.path.join('pdfs', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return redirect(url_for('generar_pdf_page'))

# ====== RUTAS API PARA CREAR REGISTROS EN MAESTRAS ======

@app.route('/api/crear-centro-costo', methods=['POST'])
def crear_centro_costo():
    """Crear un nuevo centro de costo"""
    try:
        data = request.json
        codigo_costo = data.get('codigo_costo', '').strip()
        casino = data.get('casino', '').strip()
        ruta = data.get('ruta', '').strip()
        
        if not codigo_costo or not casino:
            return jsonify({'success': False, 'message': 'Código y Casino son obligatorios'}), 400
        
        resultado = maestras_manager.crear_centro_costo(codigo_costo, casino, ruta)
        
        if resultado:
            return jsonify({'success': True, 'message': 'Centro de Costo creado exitosamente'})
        else:
            return jsonify({'success': False, 'message': 'El centro de costo ya existe'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/crear-chofer', methods=['POST'])
def crear_chofer():
    """Crear un nuevo chofer"""
    try:
        data = request.json
        nombre = data.get('nombre', '').strip().upper()
        rut = data.get('rut', '').strip()
        celular = data.get('celular', '').strip()
        
        if not nombre or not rut:
            return jsonify({'success': False, 'message': 'Nombre y RUT son obligatorios'}), 400
        
        resultado = maestras_manager.crear_chofer(nombre, rut, celular)
        
        if resultado:
            return jsonify({'success': True, 'message': 'Chofer creado exitosamente'})
        else:
            return jsonify({'success': False, 'message': 'El chofer ya existe (RUT duplicado)'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/crear-administrativo', methods=['POST'])
def crear_administrativo():
    """Crear un nuevo administrativo"""
    try:
        data = request.json
        nombre = data.get('nombre', '').strip().upper()
        
        if not nombre:
            return jsonify({'success': False, 'message': 'Nombre es obligatorio'}), 400
        
        resultado = maestras_manager.crear_administrativo(nombre)
        
        if resultado:
            return jsonify({'success': True, 'message': 'Administrativo creado exitosamente'})
        else:
            return jsonify({'success': False, 'message': 'El administrativo ya existe'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/listar-administrativos')
def listar_administrativos():
    """Listar todos los nombres de administrativos"""
    try:
        nombres = maestras_manager.listar_administrativos_nombres()
        return jsonify({'success': True, 'administrativos': nombres})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('pdfs', exist_ok=True)
    
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n" + "="*60)
    print("🚀 Sistema de Viajes DHL - Servidor Producción")
    print("="*60)
    print(f"\n📍 Acceso LOCAL (esta PC):")
    print(f"   http://localhost:5000")
    print(f"   http://127.0.0.1:5000")
    print(f"\nAcceso RED LOCAL (otras PCs en la red):")
    print(f"   http://{local_ip}:5000")
    print(f"\n👥 Usuarios simultáneos: 10")
    print(f"💾 Base de datos: SQLite con WAL mode (viajes.db)")
    print(f"Servidor: Waitress (producción)")
    print("\n" + "="*60 + "\n")
    
    # Usar Waitress para producción (más estable que Flask development server)
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000, threads=10)
    except ImportError:
        print("Waitress no instalado. Usando Flask development server...")
        print("   Para producción ejecuta: pip install waitress\n")
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            threaded=True,
            use_reloader=False
        )
