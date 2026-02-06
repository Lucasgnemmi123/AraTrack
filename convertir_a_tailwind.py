"""
Script para convertir formularios de Bootstrap a Tailwind CSS
"""
import re

def convertir_bootstrap_a_tailwind(contenido):
    """Convierte clases de Bootstrap a Tailwind CSS"""
    
    # Reemplazos de clases comunes
    reemplazos = [
        # Cards
        (r'<div class="card shadow-sm mb-4">', '<div class="bg-white rounded-xl shadow-lg mb-6 overflow-hidden">'),
        (r'<div class="card-header bg-light">', '<div class="bg-gradient-to-r from-gray-700 to-gray-800 px-6 py-4">'),
        (r'<div class="card-header bg-danger text-white">', '<div class="bg-gradient-to-r from-red-500 to-red-600 px-6 py-4">'),
        (r'<div class="card-header bg-primary text-white">', '<div class="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">'),
        (r'<div class="card-header bg-success text-white">', '<div class="bg-gradient-to-r from-green-500 to-green-600 px-6 py-4">'),
        (r'<div class="card-body">', '<div class="p-6">'),
        (r'<h5 class="mb-0"><i class="bi bi-([\w-]+) me-2"></i>', r'<h5 class="text-lg font-semibold text-white flex items-center"><i class="bi bi-\1 mr-2"></i>'),
        
        # Grid system
        (r'<div class="row g-3">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">'),
        (r'<div class="col-md-6">', '<div>'),
        (r'<div class="col-md-4">', '<div>'),
        (r'<div class="col-md-3">', '<div>'),
        (r'<div class="col-md-12">', '<div class="md:col-span-2">'),
        (r'<div class="col-12">', '<div class="md:col-span-2">'),
        
        # Forms
        (r'<label for="([\w_]+)" class="form-label">', r'<label for="\1" class="block text-sm font-medium text-gray-700 mb-2">'),
        (r'<input type="text" class="form-control"', r'<input type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"'),
        (r'<input type="date" class="form-control"', r'<input type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"'),
        (r'<input type="datetime-local" class="form-control"', r'<input type="datetime-local" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"'),
        (r'<input type="number" class="form-control"', r'<input type="number" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"'),
        (r'<input type="time" class="form-control"', r'<input type="time" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"'),
        (r'<select (.*?) class="form-select', r'<select \1 class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'),
        (r'<textarea (.*?) class="form-control', r'<textarea \1 class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'),
        
        # Readonly inputs
        (r'class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"(.*?)readonly', r'class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"\1readonly'),
        
        # Input groups
        (r'<div class="input-group">', '<div class="flex gap-2">'),
        
        # Buttons
        (r'<button type="button"(.*?)class="btn btn-primary"', r'<button type="button"\1class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"'),
        (r'<button type="button"(.*?)class="btn btn-success"', r'<button type="button"\1class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"'),
        (r'<button type="button"(.*?)class="btn btn-danger"', r'<button type="button"\1class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"'),
        (r'<button type="button"(.*?)class="btn btn-warning"', r'<button type="button"\1class="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg transition-colors"'),
        (r'<button type="button"(.*?)class="btn btn-secondary"', r'<button type="button"\1class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors"'),
        (r'<button type="submit"(.*?)class="btn btn-primary btn-lg"', r'<button type="submit"\1class="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-4 rounded-lg transition-all duration-200 text-lg shadow-lg"'),
        
        # Text utilities
        (r'<span class="text-danger">', '<span class="text-red-500">'),
        (r'<small class="text-muted">', '<small class="text-gray-500 text-xs mt-1 block">'),
        (r'class="text-uppercase"', 'class="uppercase"'),
        
        # Icons
        (r' me-1', ' mr-1'),
        (r' me-2', ' mr-2'),
        (r' me-3', ' mr-3'),
        (r' ms-2', ' ml-2'),
    ]
    
    for patron, reemplazo in reemplazos:
        contenido = re.sub(patron, reemplazo, contenido)
    
    return contenido


def procesar_archivo(ruta_archivo):
    """Procesa un archivo HTML y lo convierte a Tailwind"""
    print(f"Procesando {ruta_archivo}...")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    contenido_nuevo = convertir_bootstrap_a_tailwind(contenido)
    
    # Backup
    with open(f"{ruta_archivo}.backup", 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)
    
    print(f"✓ {ruta_archivo} convertido exitosamente")


if __name__ == "__main__":
    archivos = [
        "templates/nuevo_viaje.html",
        "templates/editar_viaje.html"
    ]
    
    for archivo in archivos:
        try:
            procesar_archivo(archivo)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")
    
    print("\n✓ Conversión completada!")
