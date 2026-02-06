"""
Script mejorado para convertir COMPLETAMENTE formularios a Tailwind CSS
"""
import re

def convertir_completo_tailwind(html):
    """Convierte TODO el HTML a Tailwind CSS profesional"""
    
    # 1. FORM-ROW -> Grid de 3 columnas
    html = re.sub(
        r'<div class="form-row">\s*',
        '<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">\n            ',
        html
    )
    
    # 2. FORM-GROUP -> Div simple
    html = re.sub(r'<div class="form-group">', '<div>', html)
    
    # 3. LABELS sin clase -> Tailwind labels
    html = re.sub(
        r'<label for="([^"]*)">(.*?)</label>',
        r'<label for="\1" class="block text-sm font-medium text-gray-700 mb-2">\2</label>',
        html
    )
    html = re.sub(
        r'<label>\s*<input',
        r'<label class="flex items-center space-x-2 text-sm text-gray-700"><input',
        html
    )
    
    # 4. INPUTS sin clase -> Tailwind inputs
    html = re.sub(
        r'<input type="text" id="([^"]*)" name="([^"]*)"([^>]*)>',
        r'<input type="text" id="\1" name="\2" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"\3>',
        html
    )
    html = re.sub(
        r'<input type="number" id="([^"]*)" name="([^"]*)"([^>]*)>',
        r'<input type="number" id="\1" name="\2" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"\3>',
        html
    )
    
    # 5. CHECKBOXES
    html = re.sub(
        r'<input type="checkbox" id="([^"]*)" name="([^"]*)"([^>]*)>',
        r'<input type="checkbox" id="\1" name="\2" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"\3>',
        html
    )
    
    # 6. H3 con estilo inline -> Tailwind
    html = re.sub(
        r'<h3 style="color: #d40511; margin-top: 1\.5rem;">(.*?)</h3>',
        r'<div class="bg-white rounded-xl shadow-lg mb-6 overflow-hidden"><div class="bg-gradient-to-r from-red-500 to-red-600 px-6 py-4"><h3 class="text-lg font-semibold text-white flex items-center"><i class="bi bi-box-arrow-right mr-2"></i>\1</h3></div><div class="p-6">',
        html
    )
    
    # 7. H4 con estilo inline -> Tailwind subtitle
    html = re.sub(
        r'<h4 style="margin-top: 1rem;">(.*?)</h4>',
        r'<h4 class="text-md font-semibold text-gray-800 mb-3 mt-6 flex items-center"><i class="bi bi-caret-right-fill text-blue-500 mr-2"></i>\1</h4>',
        html
    )
    html = re.sub(
        r'<h4>(.*?)</h4>',
        r'<h4 class="text-md font-semibold text-gray-800 mb-3 flex items-center"><i class="bi bi-caret-right-fill text-blue-500 mr-2"></i>\1</h4>',
        html
    )
    
    # 8. SELECT sin clase -> Tailwind select
    html = re.sub(
        r'<select id="([^"]*)" name="([^"]*)"([^>]*?)style="flex: 1;"',
        r'<select id="\1" name="\2" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"',
        html
    )
    
    # 9. BOTONES con estilo inline -> Tailwind
    html = re.sub(
        r'<button type="button"([^>]*?)style="padding: 0\.75rem 1rem; background: #28a745; white-space: nowrap;"',
        r'<button type="button"\1class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors whitespace-nowrap"',
        html
    )
    html = re.sub(
        r'<button type="submit" class="btn btn-primary">',
        r'<button type="submit" class="w-full md:w-auto px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-lg transition-all duration-200 text-lg shadow-lg">',
        html
    )
    
    # 10. DIV con display flex inline -> Tailwind
    html = re.sub(
        r'<div style="display: flex; gap: 0\.5rem;">',
        r'<div class="flex gap-2">',
        html
    )
    html = re.sub(
        r'<div style="display: flex; gap: 1rem; margin-top: 1\.5rem;">',
        r'<div class="flex gap-4 mt-6">',
        html
    )
    
    # 11. FORM-ACTIONS
    html = re.sub(
        r'<div class="form-actions"([^>]*)>',
        r'<div class="flex gap-4 mt-8 justify-end">',
        html
    )
    
    # 12. FORM-SECTION-HEADER
    html = re.sub(
        r'<div class="form-section-header">',
        r'<div class="bg-white rounded-xl shadow-lg mb-6 overflow-hidden"><div class="bg-gradient-to-r from-green-500 to-green-600 px-6 py-4 flex justify-between items-center">',
        html
    )
    
    # 13. HR
    html = re.sub(
        r'<hr style="[^"]*">',
        r'<div class="my-8 border-t-2 border-gray-200"></div>',
        html
    )
    
    # 14. Párrafos con estilo
    html = re.sub(
        r'<p style="color: #666; margin-bottom: 1rem;">',
        r'<p class="text-gray-600 mb-4">',
        html
    )
    
    # 15. Cerrar divs de secciones H3 (agregar cierre)
    # Esto se hace manualmente después
    
    return html

def procesar_archivo_completo(ruta):
    """Procesa archivo y convierte TODO a Tailwind"""
    print(f"\nProcesando {ruta}...")
    
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Backup
    with open(f"{ruta}.backup2", 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    contenido_nuevo = convertir_completo_tailwind(contenido)
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)
    
    print(f"✓ Conversión completa aplicada a {ruta}")

if __name__ == "__main__":
    archivos = [
        "templates/nuevo_viaje.html",
        "templates/editar_viaje.html"
    ]
    
    for archivo in archivos:
        try:
            procesar_archivo_completo(archivo)
        except Exception as e:
            print(f"❌ Error en {archivo}: {e}")
    
    print("\n✅ Conversión completa terminada!")
