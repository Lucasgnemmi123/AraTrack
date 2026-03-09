"""
Generador de PDFs de Documentación
Convierte archivos .md en PDFs visuales y fáciles de entender
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os
import re
from datetime import datetime

class DocPDFGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.docs_dir = os.path.join(self.base_dir, '_documentacion')
        self.output_dir = os.path.join(self.docs_dir, 'pdfs')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
        
    def _crear_estilos_personalizados(self):
        """Crear estilos visuales y atractivos"""
        # Título principal - GRANDE Y LLAMATIVO
        self.styles.add(ParagraphStyle(
            name='TituloGrande',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#FF6B35'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Título sección - Naranja
        self.styles.add(ParagraphStyle(
            name='TituloSeccion',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#FF8C42'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=2,
            borderColor=colors.HexColor('#FF8C42'),
            borderPadding=8,
            backColor=colors.HexColor('#FFF5F0')
        ))
        
        # Subtítulo - Azul
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2C5F8D'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal - GRANDE para fácil lectura
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=16,
            spaceAfter=8,
            alignment=TA_JUSTIFY
        ))
        
        # Código/Comando - Fondo gris con mejor padding
        self.styles.add(ParagraphStyle(
            name='Codigo',
            parent=self.styles['Code'],
            fontSize=8,
            fontName='Courier',
            backColor=colors.HexColor('#F5F5F5'),
            borderWidth=1.5,
            borderColor=colors.HexColor('#CCCCCC'),
            borderPadding=8,
            leftIndent=15,
            rightIndent=15,
            spaceAfter=12,
            leading=11
        ))
        
        # Alerta/Importante - Rojo
        self.styles.add(ParagraphStyle(
            name='Alerta',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#D62828'),
            backColor=colors.HexColor('#FFF0F0'),
            borderWidth=2,
            borderColor=colors.HexColor('#D62828'),
            borderPadding=10,
            fontName='Helvetica-Bold',
            spaceAfter=15
        ))
        
        # Éxito/Completado - Verde
        self.styles.add(ParagraphStyle(
            name='Exito',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2D6A4F'),
            backColor=colors.HexColor('#F0FFF4'),
            borderWidth=2,
            borderColor=colors.HexColor('#52B788'),
            borderPadding=10,
            fontName='Helvetica-Bold',
            spaceAfter=15
        ))
        
        # Info - Azul
        self.styles.add(ParagraphStyle(
            name='Info',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#023E8A'),
            backColor=colors.HexColor('#F0F8FF'),
            borderWidth=2,
            borderColor=colors.HexColor('#0077B6'),
            borderPadding=10,
            spaceAfter=15
        ))
    
    def _es_diagrama_ascii(self, line):
        """Detectar si una línea es parte de un diagrama ASCII art"""
        caracteres_diagrama = ['┌', '─', '┐', '│', '└', '┘', '├', '┤', '┬', '┴', '┼',
                               '╔', '═', '╗', '║', '╚', '╝', '╠', '╣', '╦', '╩', '╬',
                               '→', '↓', '←', '↑', '↔', '↕', '▼', '▲', '◄', '►', '●', '○',
                               '☐', '☑', '✓', '✗', '•', '◦']
        return any(char in line for char in caracteres_diagrama) and len(line) > 5
    
    def _crear_tabla_diagrama(self, lineas_diagrama):
        """Crear tabla bonita para diagrama ASCII"""
        texto_diagrama = '\n'.join(lineas_diagrama)
        
        # Crear tabla con el diagrama
        data = [[Paragraph(f'<font face="Courier" size="7"><pre>{texto_diagrama}</pre></font>', 
                          self.styles['Normal'])]]
        
        tabla = Table(data, colWidths=[6.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F8F8')),
            ('BORDER', (0, 0), (-1, -1), 2, colors.HexColor('#FF8C42')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return tabla
    
    def _omitir_seccion(self, titulo):
        """Detectar si una sección debe omitirse del PDF"""
        secciones_omitir = [
            'ATAJOS DE TECLADO',
            'SHORTCUTS',
            'KEYBOARD SHORTCUTS'
        ]
        return any(omit in titulo.upper() for omit in secciones_omitir)
    
    def _parse_markdown(self, md_file):
        """Parsear archivo Markdown y convertir a elementos PDF"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        elements = []
        lines = content.split('\n')
        
        i = 0
        omitir_hasta_proxima_seccion = False
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Título principal (# )
            if line.startswith('# '):
                titulo = line[2:].strip()
                elements.append(Paragraph(titulo, self.styles['TituloGrande']))
                elements.append(Spacer(1, 10*mm))
                omitir_hasta_proxima_seccion = False
            
            # Título sección (## )
            elif line.startswith('## '):
                titulo = line[3:].strip()
                
                # Verificar si es una sección a omitir
                if self._omitir_seccion(titulo):
                    omitir_hasta_proxima_seccion = True
                    i += 1
                    continue
                
                omitir_hasta_proxima_seccion = False
                
                # Salto de página antes de cada sección principal
                if len(elements) > 5:
                    elements.append(PageBreak())
                elements.append(Paragraph(f"📋 {titulo}", self.styles['TituloSeccion']))
            
            # Si estamos omitiendo, saltar hasta próxima sección
            elif omitir_hasta_proxima_seccion:
                i += 1
                continue
            
            # Subtítulo (### )
            elif line.startswith('### '):
                subtitulo = line[4:].strip()
                elements.append(Paragraph(f"▸ {subtitulo}", self.styles['Subtitulo']))
            
            # Detectar inicio de diagrama ASCII
            elif self._es_diagrama_ascii(line):
                diagrama_lines = []
                while i < len(lines) and (self._es_diagrama_ascii(lines[i]) or lines[i].strip() == ''):
                    if lines[i].strip():
                        diagrama_lines.append(lines[i].rstrip())
                    i += 1
                i -= 1
                
                if diagrama_lines:
                    elements.append(self._crear_tabla_diagrama(diagrama_lines))
                    elements.append(Spacer(1, 5*mm))
            
            # Código (```)
            elif line.startswith('```'):
                i += 1
                codigo = []
                lenguaje = line[3:].strip()
                
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    codigo.append(lines[i])
                    i += 1
                
                codigo_texto = '\n'.join(codigo)
                
                # Limitar a 35 líneas para no desbordar página
                if len(codigo) > 35:
                    codigo_texto = '\n'.join(codigo[:35]) + '\n\n... (codigo truncado, ver archivo original)'
                
                # Título del bloque de código
                if lenguaje:
                    elements.append(Paragraph(f'<b>Código ({lenguaje}):</b>', self.styles['Normal']))
                
                elements.append(Paragraph(f"<pre>{self._escape_html(codigo_texto)}</pre>", self.styles['Codigo']))
            
            # Lista con viñetas (- o *)
            elif line.startswith('- ') or line.startswith('* '):
                texto = line[2:].strip()
                # Detectar alertas especiales
                if texto.startswith('**'):
                    elements.append(Paragraph(f"→ {self._escape_html(texto)}", self.styles['Exito']))
                else:
                    elements.append(Paragraph(f"  • {self._escape_html(texto)}", self.styles['TextoNormal']))
            
            # Lista numerada
            elif re.match(r'^\d+\. ', line):
                texto = re.sub(r'^\d+\. ', '', line).strip()
                elements.append(Paragraph(f"  {texto}", self.styles['TextoNormal']))
            
            # Alerta (línea con ✅ ❌ ⚠️)
            elif '✅' in line or '[OK]' in line or 'Completed' in line.lower():
                elements.append(Paragraph(f"✓ {self._escape_html(line.replace('✅', '').replace('[OK]', ''))}", self.styles['Exito']))
            elif '❌' in line or '[!]' in line or 'Error' in line:
                elements.append(Paragraph(f"✗ {self._escape_html(line.replace('❌', '').replace('[!]', ''))}", self.styles['Alerta']))
            elif '⚠️' in line or 'Warning' in line or 'Importante' in line:
                elements.append(Paragraph(f"ℹ {self._escape_html(line.replace('⚠️', ''))}", self.styles['Info']))
            
            # Tabla Markdown (| ... |)
            elif line.startswith('|'):
                tabla_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    tabla_lines.append(lines[i].strip())
                    i += 1
                i -= 1
                if len(tabla_lines) > 1:
                    elements.append(self._crear_tabla_from_markdown(tabla_lines))
            
            # Separador horizontal (---)
            elif line.startswith('---') or line.startswith('==='):
                elements.append(Spacer(1, 5*mm))
            
            # Texto normal (no vacío)
            elif line:
                # Detectar títulos en texto
                if line.isupper() and len(line) < 60 and len(line) > 5:
                    elements.append(Paragraph(f'<b>{line}</b>', self.styles['Subtitulo']))
                else:
                    elements.append(Paragraph(self._escape_html(line), self.styles['TextoNormal']))
            
            # Línea vacía - espacio
            else:
                elements.append(Spacer(1, 3*mm))
            
            i += 1
        
        return elements
    
    def _crear_tabla_from_markdown(self, tabla_lines):
        """Convertir tabla Markdown a ReportLab Table"""
        # Parsear filas
        rows = []
        for line in tabla_lines:
            # Quitar | inicial y final
            line = line.strip('|')
            cells = [cell.strip() for cell in line.split('|')]
            rows.append(cells)
        
        # Remover línea separadora (---)
        if len(rows) > 1 and all('---' in cell or '===' in cell for cell in rows[1]):
            rows.pop(1)
        
        # Limitar ancho de celdas y ajustar según número de columnas
        if len(rows) > 0:
            num_cols = len(rows[0])
            
            # Ajustar ancho según columnas
            if num_cols <= 2:
                col_widths = [3.25*inch] * num_cols
            elif num_cols == 3:
                col_widths = [2.17*inch] * num_cols
            elif num_cols == 4:
                col_widths = [1.625*inch] * num_cols
            elif num_cols == 5:
                col_widths = [1.3*inch] * num_cols
            else:
                col_widths = [6.5*inch / num_cols] * num_cols
        else:
            col_widths = None
        
        # Truncar texto muy largo en celdas
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if len(cell) > 80 and i > 0:  # No truncar headers
                    cell = cell[:77] + '...'
                    rows[i][j] = cell
        
        # Crear tabla
        tabla = Table(rows, colWidths=col_widths, repeatRows=1)
        
        # Estilo visual mejorado
        tabla.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF8C42')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Cuerpo
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#FF8C42')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFAF5'), colors.white]),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        return tabla
    
    def _escape_html(self, text):
        """Escapar caracteres HTML y Markdown"""
        # Primero procesar negritas (**texto**)
        import re
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        
        # Procesar código inline (`texto`)
        text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
        
        # Escapar caracteres HTML (después del procesamiento de Markdown)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Re-aplicar tags HTML que ya procesamos
        text = text.replace('&lt;b&gt;', '<b>')
        text = text.replace('&lt;/b&gt;', '</b>')
        text = text.replace('&lt;font face="Courier"&gt;', '<font face="Courier">')
        text = text.replace('&lt;/font&gt;', '</font>')
        
        return text
    
    def _crear_portada(self, titulo, subtitulo):
        """Crear portada atractiva"""
        elements = []
        
        # Espaciado superior
        elements.append(Spacer(1, 2*inch))
        
        # Título principal
        elements.append(Paragraph(titulo, self.styles['TituloGrande']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtítulo
        style_subtitulo = ParagraphStyle(
            name='Subtitulo_Portada',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#2C5F8D'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        elements.append(Paragraph(subtitulo, style_subtitulo))
        elements.append(Spacer(1, 1*inch))
        
        # Info del documento
        info_style = ParagraphStyle(
            name='Info_Portada',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        
        fecha = datetime.now().strftime('%d de %B de %Y')
        elements.append(Paragraph(f"Sistema de Viajes DHL", info_style))
        elements.append(Paragraph(f"Generado: {fecha}", info_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Logo simulado (texto grande)
        logo_style = ParagraphStyle(
            name='Logo',
            parent=self.styles['Normal'],
            fontSize=48,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#FF0000'),
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph("DHL", logo_style))
        
        elements.append(PageBreak())
        return elements
    
    def generar_pdf(self, md_file, titulo, subtitulo):
        """Generar PDF desde archivo Markdown"""
        try:
            print(f"\n[+] Procesando: {os.path.basename(md_file)}")
            
            # Nombre del PDF de salida
            nombre_base = os.path.splitext(os.path.basename(md_file))[0]
            pdf_file = os.path.join(self.output_dir, f"{nombre_base}.pdf")
            
            # Crear documento
            doc = SimpleDocTemplate(
                pdf_file,
                pagesize=letter,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=15*mm,
                bottomMargin=15*mm
            )
            
            # Construir contenido
            story = []
            
            # Portada
            story.extend(self._crear_portada(titulo, subtitulo))
            
            # Contenido del documento
            story.extend(self._parse_markdown(md_file))
            
            # Generar PDF
            doc.build(story)
            
            print(f"[OK] PDF generado: {pdf_file}")
            return pdf_file
            
        except Exception as e:
            print(f"[ERROR] Error generando PDF de {md_file}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def generar_todos_los_pdfs(self):
        """Generar PDFs de toda la documentación"""
        documentos = [
            {
                'archivo': 'ARQUITECTURA_APLICACION.md',
                'titulo': 'ARQUITECTURA DE LA APLICACION',
                'subtitulo': 'Guía completa de componentes y estructura del sistema'
            },
            {
                'archivo': 'SERVIDOR_DOCUMENTACION.md',
                'titulo': 'DOCUMENTACION DEL SERVIDOR',
                'subtitulo': 'Configuración y uso de Waitress + Flask'
            },
            {
                'archivo': 'INTERFAZ_USO.md',
                'titulo': 'GUIA DE USO DE LA INTERFAZ',
                'subtitulo': 'Manual completo para usuarios del sistema web'
            },
            {
                'archivo': 'DIAGRAMAS_FLUJO.md',
                'titulo': 'DIAGRAMAS DE FLUJO',
                'subtitulo': 'Procesos y flujos del sistema visualizados'
            },
            {
                'archivo': 'ESTRUCTURA_BD.md',
                'titulo': 'ESTRUCTURA DE BASE DE DATOS',
                'subtitulo': 'Esquema relacional completo de SQLite'
            }
        ]
        
        print("="*60)
        print("GENERADOR DE PDFs - DOCUMENTACION SISTEMA VIAJES DHL")
        print("="*60)
        
        generados = []
        errores = []
        
        for doc in documentos:
            md_path = os.path.join(self.docs_dir, doc['archivo'])
            if os.path.exists(md_path):
                resultado = self.generar_pdf(md_path, doc['titulo'], doc['subtitulo'])
                if resultado:
                    generados.append(resultado)
                else:
                    errores.append(doc['archivo'])
            else:
                print(f"[!] Archivo no encontrado: {doc['archivo']}")
                errores.append(doc['archivo'])
        
        print("\n" + "="*60)
        print(f"RESUMEN: {len(generados)} PDFs generados, {len(errores)} errores")
        print("="*60)
        
        if generados:
            print("\n[OK] PDFs generados exitosamente:")
            for pdf in generados:
                print(f"     - {os.path.basename(pdf)}")
        
        if errores:
            print("\n[!] Errores en:")
            for err in errores:
                print(f"     - {err}")
        
        print(f"\n[i] Carpeta de salida: {self.output_dir}")
        return generados

if __name__ == '__main__':
    generator = DocPDFGenerator()
    generator.generar_todos_los_pdfs()
    print("\n[ENTER para cerrar]")
    input()
