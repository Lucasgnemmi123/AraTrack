"""
PDF Generator - Planilla Control Despacho DHL
Generación de PDF con formato exacto similar a la imagen
Una página por centro de costo
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
import io
import os
import sys
from datetime import datetime
from db_manager import DBManager

class PDFGenerator:
    def __init__(self):
        self.db_manager = DBManager()
        # Determinar el directorio base correcto
        if getattr(sys, 'frozen', False):
            # Corriendo como ejecutable empaquetado
            self.base_dir = os.path.dirname(sys.executable)
        else:
            # Corriendo como script normal
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def generar_pdf_viaje(self, viaje_dict, comidas_list):
        """Generar PDF para un viaje específico (método principal usado por app_web.py)"""
        try:
            # Crear buffer
            buffer = io.BytesIO()
            
            # Crear documento - Tamaño carta con márgenes mínimos
            doc = SimpleDocTemplate(
                buffer, 
                pagesize=letter,
                rightMargin=8*mm, 
                leftMargin=8*mm,
                topMargin=5*mm, 
                bottomMargin=5*mm
            )
            
            # Generar contenido
            content = self._crear_pagina_planilla(viaje_dict, comidas_list)
            
            # Construir PDF
            doc.build(content)
            
            # Guardar en carpeta pdfs junto al ejecutable o script
            pdfs_dir = os.path.join(self.base_dir, 'pdfs')
            os.makedirs(pdfs_dir, exist_ok=True)
            filename = f"viaje_{viaje_dict['numero_viaje']}_{viaje_dict['costo_codigo']}.pdf"
            filepath = os.path.join(pdfs_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(buffer.getvalue())
            
            return filepath
            
        except Exception as e:
            print(f"Error generando PDF: {str(e)}")
            return None
    
    def _crear_pagina_planilla(self, v, comidas):
        """Crear contenido completo de una página - SEGÚN IMAGEN DE REFERENCIA"""
        content = []
        
        # Función auxiliar para obtener valor
        def get(key, default=''):
            val = v.get(key, default)
            return val if val else default
        
        # Función auxiliar para valores numéricos: no mostrar 0
        def get_num(key, default=''):
            val = v.get(key, default)
            if val == 0 or val == '0' or val == '' or val is None:
                return ''
            return str(val)
        
        # 1. ENCABEZADO
        encabezado = Table([
            ['PLANILLA CONTROL DESPACHO', 'VIAJE', get('numero_viaje')]
        ], colWidths=[5*inch, 0.8*inch, 1.7*inch])
        
        encabezado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#808080')),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#D0D0D0')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        content.append(encabezado)
        content.append(Spacer(1, 1*mm))
        
        # 2. INFO GENERAL - 8 FILAS
        info = Table([
            ['CASINO', get('casino'), 'C.COSTO', get('costo_codigo')],
            ['RUTA', get('ruta'), 'PATENTE CAMION', get('patente_camion')],
            ['FECHA', get('fecha'), 'PATENTE SEMI', get('patente_semi')],
            ['PESO', get('peso_camion'), 'TIPO CAMION', get('tipo_camion')],
            ['TERMOGRAFOS', get('termografos_gps'), 'N° DE RAMPLA', get('numero_rampa')],
            ['CONDUCTOR', get('conductor'), 'N° CAMION', get('numero_camion')],
            ['RUT', get('rut'), 'FECHA HORA LLEGADA', get('fecha_hora_llegada_dhl')],
            ['CELULAR', get('celular'), 'FECHA HORA SALIDA', get('fecha_hora_salida_dhl')],
        ], colWidths=[1.1*inch, 3.7*inch, 0.9*inch, 1.8*inch], rowHeights=[0.25*inch] + [0.18*inch]*7)
        
        info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#D0D0D0')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONTSIZE', (0, 0), (0, -1), 5.5),
            ('FONTSIZE', (2, 0), (2, -1), 5.5),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (1, 0), (1, 0), 8),
            ('FONTSIZE', (3, 0), (3, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(info)
        content.append(Spacer(1, 1*mm))
        
        # 3. HEADER ACTIVOS SALIDA Y PALLETS POR AREA
        header_activos = Table([
            ['ACTIVOS SALIDA', '', '', '', 'PALLETS POR AREA', '']
        ], colWidths=[1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        
        header_activos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#808080')),
            ('BACKGROUND', (4, 0), (5, 0), colors.HexColor('#808080')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('SPAN', (0, 0), (3, 0)),
            ('SPAN', (4, 0), (5, 0)),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        content.append(header_activos)
        content.append(Spacer(1, 0))
        
        # 4. TABLA ACTIVOS - ALINEADA CON ANCHO TOTAL 7.5 INCHES
        activos = Table([
            ['N° WENCOS', get_num('num_wencos'), 'BIN', get_num('bin'), 'REFRIGERADO', get_num('pallets_refrigerado')],
            ['PALLETS', get_num('pallets'), 'PALLET\nNEGRO GRUESO', get_num('pallets_pl_negro_grueso'), 'CONGELADO', get_num('pallets_congelado')],
            ['PALLET\nCHEP', get_num('pallets_chep'), 'PALLET\nNEGRO ALTER.', get_num('pallets_pl_negro_alternativo'), 'ABARROTE', get_num('pallets_abarrote')],
            ['ADMIN.\nRESPONSABLE', get('administrativo_responsable'), '', '', 'WENCOS\nCONGELADO', get_num('wencos_congelado')],
            ['REVISION\nLIMPIEZA', get('revision_limpieza_camion_acciones'), '', '', 'WENCOS\nREFRIGERADO', get_num('wencos_refrigerado')],
        ], colWidths=[1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch], rowHeights=[0.30*inch]*5)
        
        activos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (2, 0), (2, 2), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (4, 0), (4, -1), colors.HexColor('#D0D0D0')),
            ('SPAN', (1, 3), (3, 3)),
            ('SPAN', (1, 4), (3, 4)),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 6.5),
            ('FONTSIZE', (2, 0), (2, -1), 6.5),
            ('FONTSIZE', (4, 0), (4, -1), 6.5),
            ('FONTSIZE', (1, 0), (1, 2), 10),
            ('FONTSIZE', (3, 0), (3, 2), 10),
            ('FONTSIZE', (5, 0), (5, -1), 10),
            ('FONTSIZE', (1, 3), (3, 3), 8),
            ('FONTSIZE', (1, 4), (3, 4), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(activos)
        content.append(Spacer(1, 1*mm))
        
        # 5. CHECKBOXES - UNA SOLA FILA
        check_congelado = 'x' if get('check_congelado') == 'X' else ''
        check_refrigerado = 'x' if get('check_refrigerado') == 'X' else ''
        check_abarrote = 'x' if get('check_abarrote') == 'X' else ''
        check_implementos = 'x' if get('check_implementos') == 'X' else ''
        check_aseo = 'x' if get('check_aseo') == 'X' else ''
        check_trazabilidad = 'x' if get('check_trazabilidad') == 'X' else ''
        check_plataforma = 'x' if get('check_plataforma_wtck') == 'X' else ''
        check_env_correo = 'x' if get('check_env_correo_wtck') == 'X' else ''
        check_revision = 'x' if get('check_revision_planilla_despacho') == 'X' else ''
        
        checks = Table([
            ['CONG.', check_congelado, 'REFRIG.', check_refrigerado, 'ABARR.', check_abarrote, 'IMPLEM.', check_implementos, 'ASEO', check_aseo, 'TRAZ.', check_trazabilidad, 'PLAT. WTCK', check_plataforma, 'ENV. WTCK', check_env_correo, 'REV. PLANILLA', check_revision],
        ], colWidths=[0.55*inch, 0.22*inch, 0.55*inch, 0.22*inch, 0.55*inch, 0.22*inch, 0.6*inch, 0.22*inch, 0.45*inch, 0.22*inch, 0.5*inch, 0.22*inch, 0.75*inch, 0.22*inch, 0.7*inch, 0.22*inch, 0.9*inch, 0.22*inch], rowHeights=[0.3*inch])
        
        checks.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (2, 0), (2, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (4, 0), (4, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (6, 0), (6, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (8, 0), (8, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (10, 0), (10, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (12, 0), (12, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (14, 0), (14, 0), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (16, 0), (16, 0), colors.HexColor('#D0D0D0')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(checks)
        content.append(Spacer(1, 1*mm))
        
        # 6. SELLOS
        sellos = Table([
            ['SELLOS', '1P', '2P', '3P', '4P', '5P'],
            ['SALIDA', get('sello_salida_1p'), get('sello_salida_2p'), get('sello_salida_3p'), get('sello_salida_4p'), get('sello_salida_5p')],
            ['ENTRADA', get('sello_retorno_1p'), get('sello_retorno_2p'), get('sello_retorno_3p'), get('sello_retorno_4p'), get('sello_retorno_5p')],
        ], colWidths=[1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        
        sellos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#D0D0D0')),
            ('BACKGROUND', (1, 0), (-1, 0), colors.HexColor('#D0D0D0')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(sellos)
        content.append(Spacer(1, 1*mm))
        
        # 7. GUÍAS
        guias_header = Table([['GUIAS']], colWidths=[7.5*inch])
        guias_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#808080')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        content.append(guias_header)
        
        guias = Table([
            [get('guia_1'), get('guia_2'), get('guia_3'), get('guia_4'), get('guia_5'), get('guia_6'), get('guia_7')],
            [get('guia_8'), get('guia_9'), get('guia_10'), get('guia_11'), get('guia_12'), get('guia_13'), get('guia_14')],
        ], colWidths=[1.07*inch] * 7)
        
        guias.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(guias)
        content.append(Spacer(1, 1*mm))
        
        # 8. COMIDAS PREPARADAS
        comidas_header = Table([['COMIDAS PREPARADAS / IMPLEMENTOS']], colWidths=[7.5*inch])
        comidas_header.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#808080')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        content.append(comidas_header)
        
        # Tabla de comidas - 20 FILAS
        comidas_data = [['GUIAS', 'PROVEEDOR', 'DESCRIPCION', 'KILO', 'BULTOS']]
        
        for comida in comidas[:20]:
            proveedor = comida.get('proveedor', '') or ''
            if len(proveedor) > 15:
                proveedor = proveedor[:15]
            descripcion = comida.get('descripcion', '') or ''
            if len(descripcion) > 20:
                descripcion = descripcion[:20]
            
            # Obtener kilo y bultos, no mostrar si es 0
            kilo = comida.get('kilo', '')
            if kilo == 0 or kilo == '0' or kilo == '' or kilo is None:
                kilo = ''
            else:
                kilo = str(kilo)
            
            bultos = comida.get('bultos', '')
            if bultos == 0 or bultos == '0' or bultos == '' or bultos is None:
                bultos = ''
            else:
                bultos = str(bultos)
            
            comidas_data.append([
                comida.get('guia_comida', '') or '',
                proveedor,
                descripcion,
                kilo,
                bultos
            ])
        
        while len(comidas_data) < 21:
            comidas_data.append(['', '', '', '', ''])
        
        comidas_table = Table(
            comidas_data, 
            colWidths=[1.2*inch, 1.6*inch, 3.5*inch, 0.6*inch, 0.6*inch],
            rowHeights=[0.18*inch] * len(comidas_data)
        )
        comidas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D0D0D0')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(comidas_table)
        content.append(Spacer(1, 1*mm))
        
        # 9. FIRMAS
        firmas = Table([
            ['NOMBRE Y FIRMA DHL', 'PORTERIA DHL', 'FIRMA CONDUCTOR', 'FIRMA RESP. CASINO\nDEVOLUCION Y RECEPCIONES'],
        ], colWidths=[1.875*inch] * 4, rowHeights=[0.2*inch])
        
        firmas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D0D0D0')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        content.append(firmas)
        
        return content
    
    def generar_pdf_completo(self, numero_viaje):
        """Generar PDF con todas las hojas (un centro de costo por hoja)"""
        try:
            # Obtener centros de costo del viaje
            centros = self.db_manager.get_centros_costo_por_viaje(numero_viaje)
            if not centros:
                return None
            
            # Crear buffer con márgenes optimizados
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer, 
                pagesize=letter,
                rightMargin=10*mm, 
                leftMargin=10*mm,
                topMargin=8*mm, 
                bottomMargin=8*mm
            )
            
            content = []
            
            # Generar una página por cada centro de costo
            for i, centro in enumerate(centros):
                if i > 0:
                    content.append(PageBreak())
                
                viaje_dict = self.db_manager.get_viaje_por_numero_y_centro(numero_viaje, centro)
                comidas_list = self.db_manager.get_comidas_por_viaje_y_centro(numero_viaje, centro)
                
                if viaje_dict:
                    content.extend(self._crear_pagina_planilla(viaje_dict, comidas_list))
            
            # Construir PDF
            doc.build(content)
            
            # Guardar en carpeta pdfs junto al ejecutable o script
            pdfs_dir = os.path.join(self.base_dir, 'pdfs')
            os.makedirs(pdfs_dir, exist_ok=True)
            filename = f"viaje_{numero_viaje}_completo.pdf"
            filepath = os.path.join(pdfs_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(buffer.getvalue())
            
            return filepath
            
        except Exception as e:
            print(f"Error generando PDF completo: {str(e)}")
            return None
