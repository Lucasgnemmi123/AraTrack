// editar_viaje.js - VERSION 2026-02-10 COMPLETO
let numeroViajeActual = '';
let centrosCostoDisponibles = [];
let contadorComidasEdit = 0;

// PASO 1: Buscar centros de costo
function buscarCentrosCosto() {
    const numeroViaje = document.getElementById('buscar_numero_viaje').value.trim();
    const mensajeBusqueda = document.getElementById('mensaje-busqueda');
    
    console.log('>>> buscarCentrosCosto llamado, numeroViaje:', numeroViaje);
    
    if (!numeroViaje) {
        mensajeBusqueda.innerHTML = '<div class="bg-red-50 border-l-4 border-red-500 p-3 rounded"><p class="text-red-700 text-sm">Ingresa un número de viaje</p></div>';
        return;
    }
    
    numeroViajeActual = numeroViaje;
    mensajeBusqueda.innerHTML = '<div class="bg-gray-50 border-l-4 border-gray-400 p-3 rounded"><p class="text-gray-700 text-sm flex items-center"><i class="bi bi-hourglass-split mr-2 animate-spin"></i>Buscando centros de costo...</p></div>';
    
    console.log('>>> Haciendo fetch a:', `/api/buscar-centros-costo/${numeroViaje}`);
    
    fetch(`/api/buscar-centros-costo/${numeroViaje}`)
        .then(response => {
            console.log('>>> Response status:', response.status);
            console.log('>>> Response ok:', response.ok);
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            return response.json();
        })
        .then(centros => {
            console.log('>>> Centros recibidos:', centros);
            console.log('>>> Tipo:', typeof centros, 'Es array?', Array.isArray(centros));
            console.log('>>> Longitud:', centros ? centros.length : 'null/undefined');
            
            if (centros && Array.isArray(centros) && centros.length > 0) {
                centrosCostoDisponibles = centros;
                mostrarCentrosCosto(centros);
                mensajeBusqueda.innerHTML = `<div class="bg-green-50 border-l-4 border-green-500 p-3 rounded"><p class="text-green-700 text-sm flex items-center"><i class="bi bi-check-circle mr-2"></i>Se encontraron ${centros.length} centro(s) de costo</p></div>`;
            } else {
                console.log('>>> No se encontraron centros o respuesta inválida');
                mensajeBusqueda.innerHTML = `<div class="bg-yellow-50 border-l-4 border-yellow-500 p-3 rounded">
                    <p class="text-yellow-700 text-sm font-bold">No se encontraron registros para el viaje ${numeroViaje}</p>
                    <p class="text-yellow-600 text-xs mt-1">Verifica que el número de viaje exista en la base de datos.</p>
                    <p class="text-yellow-600 text-xs">Respuesta: ${JSON.stringify(centros)}</p>
                </div>`;
                document.getElementById('paso2-centros').style.display = 'none';
                document.getElementById('paso3-formulario').style.display = 'none';
            }
        })
        .catch(error => {
            console.error('>>> ERROR en fetch:', error);
            mensajeBusqueda.innerHTML = `<div class="bg-red-50 border-l-4 border-red-500 p-3 rounded">
                <p class="text-red-700 text-sm font-bold">❌ Error al buscar viaje</p>
                <p class="text-red-600 text-xs mt-1">${error.message}</p>
                <p class="text-red-600 text-xs mt-1">Verifica tu conexión o que estés logueado.</p>
            </div>`;
        });
}

// PASO 2: Mostrar centros disponibles
function mostrarCentrosCosto(centros) {
    const select = document.getElementById('select_centro_costo');
    select.innerHTML = '<option value="">Seleccionar centro de costo...</option>';
    
    centros.forEach(centro => {
        const option = document.createElement('option');
        option.value = centro.codigo;
        option.textContent = `${centro.codigo} - ${centro.casino}`;
        select.appendChild(option);
    });
    
    document.getElementById('paso2-centros').style.display = 'block';
    document.getElementById('paso3-formulario').style.display = 'none';
    document.getElementById('paso2-centros').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// PASO 3: Cargar viaje completo
function cargarViajeCompleto() {
    const centroCosto = document.getElementById('select_centro_costo').value;
    
    if (!centroCosto) {
        document.getElementById('paso3-formulario').style.display = 'none';
        return;
    }
    
    fetch('/api/buscar-viaje', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            numero_viaje: numeroViajeActual,
            centro_costo: centroCosto
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            llenarFormulario(result.viaje, result.comidas);
            document.getElementById('paso3-formulario').style.display = 'block';
            setTimeout(() => {
                document.getElementById('paso3-formulario').scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        } else {
            alert('❌ No se pudo cargar el viaje');
        }
    })
    .catch(error => {
        alert('❌ Error: ' + error.message);
    });
}

function llenarFormulario(viaje, comidas) {
    document.getElementById('info_numero_viaje').textContent = viaje.numero_viaje || '';
    document.getElementById('info_centro_costo').textContent = viaje.costo_codigo || '';
    
    const form = document.getElementById('formEditar');
    form.innerHTML = `
        <input type="hidden" id="edit_numero_viaje" value="${viaje.numero_viaje || ''}">
        <input type="hidden" id="edit_centro_costo" value="${viaje.costo_codigo || ''}">
        
        <!-- INFORMACIÓN PRINCIPAL -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-red-500 to-red-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-info-circle mr-2"></i>Información Principal del Viaje
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Número de Viaje</label>
                        <input type="text" value="${viaje.numero_viaje || ''}" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Centro de Costo</label>
                        <input type="text" value="${viaje.costo_codigo || ''}" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50">
                    </div>
                    <div>
                        <label for="edit_fecha" class="block text-sm font-medium text-gray-700 mb-1">
                            Fecha <span class="text-red-500">*</span>
                        </label>
                        <input type="date" id="edit_fecha" value="${viaje.fecha || ''}" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent">
                    </div>
                </div>
            </div>
        </div>

        <!-- CASINO Y RUTA -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-teal-500 to-teal-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-building mr-2"></i>Casino y Ruta
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                        <label for="edit_casino" class="block text-sm font-medium text-gray-700 mb-1">Casino</label>
                        <input type="text" id="edit_casino" value="${viaje.casino || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_ruta" class="block text-sm font-medium text-gray-700 mb-1">Ruta</label>
                        <input type="text" id="edit_ruta" value="${viaje.ruta || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent">
                    </div>
                </div>
            </div>
        </div>

        <!-- DATOS DEL CAMIÓN -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-truck mr-2"></i>Datos del Camión
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                        <label for="edit_tipo_camion" class="block text-sm font-medium text-gray-700 mb-1">Tipo de Camión</label>
                        <input type="text" id="edit_tipo_camion" value="${viaje.tipo_camion || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_patente_camion" class="block text-sm font-medium text-gray-700 mb-1">
                            Patente Camión <span class="text-red-500">*</span>
                        </label>
                        <input type="text" id="edit_patente_camion" value="${viaje.patente_camion || ''}" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent uppercase">
                    </div>
                    <div>
                        <label for="edit_patente_semi" class="block text-sm font-medium text-gray-700 mb-1">Patente Semi</label>
                        <input type="text" id="edit_patente_semi" value="${viaje.patente_semi || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_numero_rampa" class="block text-sm font-medium text-gray-700 mb-1">N° de Rampla</label>
                        <input type="text" id="edit_numero_rampa" value="${viaje.numero_rampa || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_peso_camion" class="block text-sm font-medium text-gray-700 mb-1">Peso Camión</label>
                        <input type="text" id="edit_peso_camion" value="${viaje.peso_camion || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_numero_camion" class="block text-sm font-medium text-gray-700 mb-1">N° Camión</label>
                        <input type="text" id="edit_numero_camion" value="${viaje.numero_camion || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                    <div class="md:col-span-2">
                        <label for="edit_termografos_gps" class="block text-sm font-medium text-gray-700 mb-1">Termógrafos / GPS</label>
                        <input type="text" id="edit_termografos_gps" value="${viaje.termografos_gps || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    </div>
                </div>
            </div>
        </div>

        <!-- DATOS DEL CONDUCTOR -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-purple-500 to-purple-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-person mr-2"></i>Datos del Conductor
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div>
                        <label for="edit_chofer" class="block text-sm font-medium text-gray-700 mb-1">
                            Conductor <span class="text-red-500">*</span>
                        </label>
                        <input type="text" id="edit_chofer" value="${viaje.conductor || ''}" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_celular" class="block text-sm font-medium text-gray-700 mb-1">Celular</label>
                        <input type="text" id="edit_celular" value="${viaje.celular || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_rut" class="block text-sm font-medium text-gray-700 mb-1">RUT</label>
                        <input type="text" id="edit_rut" value="${viaje.rut || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                    </div>
                </div>
            </div>
        </div>

        <!-- HORARIOS DHL -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-orange-500 to-orange-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-clock mr-2"></i>Horarios DHL
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                        <label for="edit_hora_llegada" class="block text-sm font-medium text-gray-700 mb-1">Fecha y Hora Llegada DHL</label>
                        <input type="datetime-local" id="edit_hora_llegada" value="${viaje.fecha_hora_llegada_dhl || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_hora_salida" class="block text-sm font-medium text-gray-700 mb-1">Fecha y Hora Salida DHL</label>
                        <input type="datetime-local" id="edit_hora_salida" value="${viaje.fecha_hora_salida_dhl || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent">
                    </div>
                </div>
            </div>
        </div>

        <!-- ACTIVOS SALIDA -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-500 to-indigo-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-box-seam mr-2"></i>Activos Salida
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                    <div>
                        <label for="edit_num_wencos" class="block text-sm font-medium text-gray-700 mb-1">N° Wencos</label>
                        <input type="number" id="edit_num_wencos" value="${viaje.num_wencos || 0}" min="0" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_bin" class="block text-sm font-medium text-gray-700 mb-1">BIN</label>
                        <input type="text" id="edit_bin" value="${viaje.bin || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets" class="block text-sm font-medium text-gray-700 mb-1">Pallets</label>
                        <input type="number" id="edit_pallets" value="${viaje.pallets || 0}" min="0" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets_chep" class="block text-sm font-medium text-gray-700 mb-1">Pallets CHEP</label>
                        <input type="number" id="edit_pallets_chep" value="${viaje.pallets_chep || 0}" min="0" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets_pl_negro_grueso" class="block text-sm font-medium text-gray-700 mb-1">Pallets PL Negro Grueso</label>
                        <input type="text" id="edit_pallets_pl_negro_grueso" value="${viaje.pallets_pl_negro_grueso || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets_pl_negro_alternativo" class="block text-sm font-medium text-gray-700 mb-1">Pallets PL Negro Alternativo</label>
                        <input type="text" id="edit_pallets_pl_negro_alternativo" value="${viaje.pallets_pl_negro_alternativo || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                </div>

                <h6 class="text-md font-semibold text-gray-800 mb-2 mt-4 flex items-center"><i class="bi bi-thermometer-half mr-2 text-blue-500"></i>Pallets por Área</h6>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                    <div>
                        <label for="edit_pallets_congelado" class="block text-sm font-medium text-gray-700 mb-1">Pallets Congelado</label>
                        <input type="number" id="edit_pallets_congelado" value="${viaje.pallets_congelado || 0}" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_wencos_congelado" class="block text-sm font-medium text-gray-700 mb-1">Wencos Congelado</label>
                        <input type="number" id="edit_wencos_congelado" value="${viaje.wencos_congelado || 0}" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets_refrigerado" class="block text-sm font-medium text-gray-700 mb-1">Pallets Refrigerado</label>
                        <input type="number" id="edit_pallets_refrigerado" value="${viaje.pallets_refrigerado || 0}" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_wencos_refrigerado" class="block text-sm font-medium text-gray-700 mb-1">Wencos Refrigerado</label>
                        <input type="number" id="edit_wencos_refrigerado" value="${viaje.wencos_refrigerado || 0}" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_pallets_abarrote" class="block text-sm font-medium text-gray-700 mb-1">Pallets Abarrote</label>
                        <input type="number" id="edit_pallets_abarrote" value="${viaje.pallets_abarrote || 0}" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                </div>

                <h6 class="text-md font-semibold text-gray-800 mb-2 mt-4 flex items-center"><i class="bi bi-check2-square mr-2 text-green-500"></i>Validaciones</h6>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-3 bg-gray-50 p-3 rounded-lg">
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_congelado" ${(viaje.check_congelado === 'X' || viaje.check_congelado === 'x' || viaje.check_congelado === '1' || viaje.check_congelado === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Congelado</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_refrigerado" ${(viaje.check_refrigerado === 'X' || viaje.check_refrigerado === 'x' || viaje.check_refrigerado === '1' || viaje.check_refrigerado === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Refrigerado</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_abarrote" ${(viaje.check_abarrote === 'X' || viaje.check_abarrote === 'x' || viaje.check_abarrote === '1' || viaje.check_abarrote === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Abarrote</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_implementos" ${(viaje.check_implementos === 'X' || viaje.check_implementos === 'x' || viaje.check_implementos === '1' || viaje.check_implementos === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Implementos</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_aseo" ${(viaje.check_aseo === 'X' || viaje.check_aseo === 'x' || viaje.check_aseo === '1' || viaje.check_aseo === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Aseo</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_trazabilidad" ${(viaje.check_trazabilidad === 'X' || viaje.check_trazabilidad === 'x' || viaje.check_trazabilidad === '1' || viaje.check_trazabilidad === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Trazabilidad</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_plataforma_wtck" ${(viaje.check_plataforma_wtck === 'X' || viaje.check_plataforma_wtck === 'x' || viaje.check_plataforma_wtck === '1' || viaje.check_plataforma_wtck === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Plataforma WTCK</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_env_correo_wtck" ${(viaje.check_env_correo_wtck === 'X' || viaje.check_env_correo_wtck === 'x' || viaje.check_env_correo_wtck === '1' || viaje.check_env_correo_wtck === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Envío Correo WTCK</span>
                    </label>
                    <label class="flex items-center space-x-2 text-sm text-gray-700 cursor-pointer hover:text-gray-900">
                        <input type="checkbox" id="edit_check_revision_planilla_despacho" ${(viaje.check_revision_planilla_despacho === 'X' || viaje.check_revision_planilla_despacho === 'x' || viaje.check_revision_planilla_despacho === '1' || viaje.check_revision_planilla_despacho === 1) ? 'checked' : ''} class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500">
                        <span class="font-medium">Revisión Planilla Despacho</span>
                    </label>
                </div>
            </div>
        </div>

        <!-- GUÍAS DE DESPACHO -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-pink-500 to-pink-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-file-text mr-2"></i>Guías de Despacho
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-7 gap-3 mb-3">
                    ${[1,2,3,4,5,6,7].map(i => `
                        <div>
                            <label for="edit_guia_${i}" class="block text-sm font-medium text-gray-700 mb-1">${i === 1 ? 'Guía de activos (Guía 1)' : `Guía ${i}`}</label>
                            <input type="text" id="edit_guia_${i}" value="${viaje[`guia_${i}`] || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent">
                        </div>
                    `).join('')}
                </div>
                <div class="grid grid-cols-1 md:grid-cols-7 gap-3 mb-3">
                    ${[8,9,10,11,12,13,14].map(i => `
                        <div>
                            <label for="edit_guia_${i}" class="block text-sm font-medium text-gray-700 mb-1">Guía ${i}</label>
                            <input type="text" id="edit_guia_${i}" value="${viaje[`guia_${i}`] || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent">
                        </div>
                    `).join('')}
                </div>
                <div class="grid grid-cols-1 md:grid-cols-7 gap-3">
                    ${[15,16,17,18,19,20,21].map(i => `
                        <div>
                            <label for="edit_guia_${i}" class="block text-sm font-medium text-gray-700 mb-1">Guía ${i}</label>
                            <input type="text" id="edit_guia_${i}" value="${viaje[`guia_${i}`] || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent">
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>

        <!-- SELLOS -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-yellow-500 to-yellow-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-lock mr-2"></i>Sellos
                </h5>
            </div>
            <div class="p-4">
                <h6 class="text-md font-semibold text-gray-700 mb-2">Sellos Salida</h6>
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3 mb-4">
                    ${[1,2,3,4,5].map(i => `
                        <div>
                            <label for="edit_sello_salida_${i}p" class="block text-sm font-medium text-gray-700 mb-1">Sello Salida ${i}</label>
                            <input type="text" id="edit_sello_salida_${i}p" value="${viaje[`sello_salida_${i}p`] || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent">
                        </div>
                    `).join('')}
                </div>

                <h6 class="text-md font-semibold text-gray-700 mb-2 mt-4">Sellos Retorno</h6>
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
                    ${[1,2,3,4,5].map(i => `
                        <div>
                            <label for="edit_sello_retorno_${i}p" class="block text-sm font-medium text-gray-700 mb-1">Sello Retorno ${i}</label>
                            <input type="text" id="edit_sello_retorno_${i}p" value="${viaje[`sello_retorno_${i}p`] || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent">
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>

        <!-- CERTIFICADOS Y REVISIÓN -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-clipboard-check mr-2"></i>Certificados y Revisión
                </h5>
            </div>
            <div class="p-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                    <div>
                        <label for="edit_numero_certificado_fumigacion" class="block text-sm font-medium text-gray-700 mb-1">N° Certificado Fumigación</label>
                        <input type="text" id="edit_numero_certificado_fumigacion" value="${viaje.numero_certificado_fumigacion || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                    </div>
                    <div>
                        <label for="edit_revision_limpieza_camion_acciones" class="block text-sm font-medium text-gray-700 mb-1">Revisión Limpieza Camión</label>
                        <input type="text" id="edit_revision_limpieza_camion_acciones" value="${viaje.revision_limpieza_camion_acciones || ''}" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                    </div>
                </div>

                <div>
                    <label for="edit_administrativo_responsable" class="block text-sm font-medium text-gray-700 mb-1">Administrativo Responsable</label>
                    <select id="edit_administrativo_responsable" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent select2">
                        <option value="">Seleccione un administrativo...</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- COMIDAS PREPARADAS / IMPLEMENTOS -->
        <div class="bg-white rounded-xl shadow-lg mb-2 overflow-hidden">
            <div class="bg-gradient-to-r from-amber-500 to-amber-600 px-4 py-2">
                <h5 class="text-lg font-semibold text-white flex items-center">
                    <i class="bi bi-egg-fried mr-2"></i>Comidas Preparadas / Implementos
                </h5>
            </div>
            <div class="p-4">
                <div id="edit-comidas-container">
                    ${comidas.map((comida, index) => `
                        <div class="comida-item-edit mb-3 p-3 bg-gray-50 rounded-lg" id="comida-edit-${index}">
                            <div class="grid grid-cols-1 md:grid-cols-7 gap-3">
                                <div class="flex items-center justify-center">
                                    <span class="comida-numero text-2xl font-bold text-green-600">#${index + 1}</span>
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">N° Guía</label>
                                    <input type="text" class="comida_guia w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="${comida.guia_comida || ''}">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
                                    <input type="text" class="comida_proveedor w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="${comida.proveedor || ''}">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Descripción <span class="text-red-500">*</span></label>
                                    <input type="text" class="comida_descripcion w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="${comida.descripcion || ''}">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Kilo</label>
                                    <input type="number" class="comida_kilo w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="${comida.kilo || 0}" step="0.01" min="0">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Bultos</label>
                                    <input type="number" class="comida_bultos w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="${comida.bultos || 0}" min="0">
                                </div>
                                <div class="flex items-end">
                                    <button type="button" onclick="eliminarComidaEdit(${index})" class="w-full px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors flex items-center justify-center">
                                        <i class="bi bi-trash mr-1"></i>Eliminar
                                    </button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <button type="button" onclick="agregarComidaEdit()" class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors flex items-center">
                    <i class="bi bi-plus-circle mr-2"></i>Agregar Comida
                </button>
            </div>
        </div>


        <div class="flex gap-3 mt-6 pt-4 border-t-2 border-gray-200">
            <button type="submit" class="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 flex items-center justify-center text-lg">
                <i class="bi bi-save mr-2"></i>Actualizar Viaje
            </button>
            <button type="button" onclick="confirmarEliminar()" class="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 flex items-center justify-center text-lg">
                <i class="bi bi-trash mr-2"></i>Eliminar Viaje
            </button>
            <button type="button" onclick="cancelarEdicion()" class="px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-semibold rounded-lg shadow-lg transition-all duration-200 flex items-center justify-center">
                <i class="bi bi-x-circle mr-2"></i>Cancelar
            </button>
        </div>
    `;
    
    contadorComidasEdit = comidas.length;
    document.getElementById('formEditar').addEventListener('submit', actualizarViaje);
    
    // Cargar administrativos en el select2
    cargarAdministrativosEdicion(viaje.administrativo_responsable || '');
}

function agregarComidaEdit() {
    // Limitar a 20 comidas máximo
    if (contadorComidasEdit >= 20) {
        alert('⚠️ Máximo 20 comidas permitidas');
        return;
    }
    
    const container = document.getElementById('edit-comidas-container');
    const nuevoIndex = document.querySelectorAll('.comida-item-edit').length;
    const numeroFila = nuevoIndex + 1;
    
    container.insertAdjacentHTML('beforeend', `
        <div class="comida-item-edit mb-3 p-3 bg-gray-50 rounded-lg" id="comida-edit-${contadorComidasEdit}">
            <div class="grid grid-cols-1 md:grid-cols-7 gap-3">
                <div class="flex items-center justify-center">
                    <span class="comida-numero text-2xl font-bold text-green-600">#${numeroFila}</span>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">N° Guía</label>
                    <input type="text" class="comida_guia w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" placeholder="N° Guía">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Proveedor</label>
                    <input type="text" class="comida_proveedor w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" placeholder="Proveedor">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Descripción <span class="text-red-500">*</span></label>
                    <input type="text" class="comida_descripcion w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" placeholder="Tipo de comida">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Kilo</label>
                    <input type="number" class="comida_kilo w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="0" step="0.01" min="0" placeholder="0.00">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Bultos</label>
                    <input type="number" class="comida_bultos w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent" value="0" min="0" placeholder="0">
                </div>
                <div class="flex items-end">
                    <button type="button" onclick="eliminarComidaEdit(${contadorComidasEdit})" class="w-full px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors flex items-center justify-center">
                        <i class="bi bi-trash mr-1"></i>Eliminar
                    </button>
                </div>
            </div>
        </div>
    `);
    contadorComidasEdit++;
    renumerarComidasEdit();
}

function renumerarComidasEdit() {
    const comidas = document.querySelectorAll('#edit-comidas-container > .comida-item-edit');
    comidas.forEach((comida, index) => {
        const numeroSpan = comida.querySelector('.comida-numero');
        if (numeroSpan) {
            numeroSpan.textContent = `#${index + 1}`;
        }
    });
}

function eliminarComidaEdit(index) {
    const elemento = document.getElementById(`comida-edit-${index}`);
    if (elemento) {
        mostrarModalConfirm(
            '¿Estás seguro de eliminar esta comida? Esta acción no se puede deshacer.',
            function(confirmado) {
                if (confirmado) {
                    elemento.remove();
                    renumerarComidasEdit();
                }
            }
        );
    }
}

function actualizarViaje(e) {
    e.preventDefault();
    
    const data = {
        numero_viaje: document.getElementById('edit_numero_viaje').value,
        centro_costo: document.getElementById('edit_centro_costo').value,
        fecha: document.getElementById('edit_fecha').value,
        casino: document.getElementById('edit_casino').value,
        ruta: document.getElementById('edit_ruta').value,
        tipo_camion: document.getElementById('edit_tipo_camion').value,
        patente_camion: document.getElementById('edit_patente_camion').value,
        patente_semi: document.getElementById('edit_patente_semi').value,
        numero_rampa: document.getElementById('edit_numero_rampa').value,
        peso_camion: document.getElementById('edit_peso_camion').value,
        numero_camion: document.getElementById('edit_numero_camion').value,
        termografos_gps: document.getElementById('edit_termografos_gps').value,
        chofer: document.getElementById('edit_chofer').value,
        celular: document.getElementById('edit_celular').value,
        rut: document.getElementById('edit_rut').value,
        hora_salida: document.getElementById('edit_hora_salida').value,
        hora_llegada: document.getElementById('edit_hora_llegada').value,
        num_wencos: document.getElementById('edit_num_wencos').value,
        bin: document.getElementById('edit_bin').value,
        pallets: document.getElementById('edit_pallets').value,
        pallets_chep: document.getElementById('edit_pallets_chep').value,
        pallets_pl_negro_grueso: document.getElementById('edit_pallets_pl_negro_grueso').value,
        pallets_pl_negro_alternativo: document.getElementById('edit_pallets_pl_negro_alternativo').value,
        pallets_congelado: document.getElementById('edit_pallets_congelado').value,
        wencos_congelado: document.getElementById('edit_wencos_congelado').value,
        check_congelado: document.getElementById('edit_check_congelado').checked ? 'X' : '',
        pallets_refrigerado: document.getElementById('edit_pallets_refrigerado').value,
        wencos_refrigerado: document.getElementById('edit_wencos_refrigerado').value,
        check_refrigerado: document.getElementById('edit_check_refrigerado').checked ? 'X' : '',
        pallets_abarrote: document.getElementById('edit_pallets_abarrote').value,
        check_abarrote: document.getElementById('edit_check_abarrote').checked ? 'X' : '',
        check_implementos: document.getElementById('edit_check_implementos').checked ? 'X' : '',
        check_aseo: document.getElementById('edit_check_aseo').checked ? 'X' : '',
        check_trazabilidad: document.getElementById('edit_check_trazabilidad').checked ? 'X' : '',
        check_plataforma_wtck: document.getElementById('edit_check_plataforma_wtck').checked ? 'X' : '',
        check_env_correo_wtck: document.getElementById('edit_check_env_correo_wtck').checked ? 'X' : '',
        check_revision_planilla_despacho: document.getElementById('edit_check_revision_planilla_despacho').checked ? 'X' : '',
        numero_certificado_fumigacion: document.getElementById('edit_numero_certificado_fumigacion').value,
        revision_limpieza_camion_acciones: document.getElementById('edit_revision_limpieza_camion_acciones').value,
        administrativo_responsable: document.getElementById('edit_administrativo_responsable').value,
        comidas: []
    };
    
    for (let i = 1; i <= 21; i++) {
        data[`guia_${i}`] = document.getElementById(`edit_guia_${i}`).value;
    }
    
    for (let i = 1; i <= 5; i++) {
        data[`sello_salida_${i}p`] = document.getElementById(`edit_sello_salida_${i}p`).value;
        data[`sello_retorno_${i}p`] = document.getElementById(`edit_sello_retorno_${i}p`).value;
    }
    
    const comidasItems = document.querySelectorAll('.comida-item-edit');
    comidasItems.forEach(item => {
        const descripcion = item.querySelector('.comida_descripcion').value.trim();
        if (descripcion) {
            data.comidas.push({
                guia_comida: item.querySelector('.comida_guia').value,
                proveedor: item.querySelector('.comida_proveedor').value,
                descripcion: descripcion,
                kilo: parseFloat(item.querySelector('.comida_kilo').value) || 0,
                bultos: parseInt(item.querySelector('.comida_bultos').value) || 0
            });
        }
    });
    
    fetch('/api/actualizar-viaje', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            window.viajeActualizadoExitoso = true;
            mostrarModalInfo(
                'VIAJE ACTUALIZADO',
                `El viaje ${data.numero_viaje} ha sido actualizado exitosamente. La página se recargará para buscar otro viaje.`,
                'success'
            );
        } else {
            mostrarModalInfo(
                'ERROR AL ACTUALIZAR',
                result.message || 'No se pudo actualizar el viaje. Por favor, intenta nuevamente.',
                'error'
            );
        }
    })
    .catch(error => {
        mostrarModalInfo(
            'ERROR DE CONEXIÓN',
            'No se pudo conectar con el servidor. Verifica tu conexión e intenta nuevamente.',
            'error'
        );
    });
}

function confirmarEliminar() {
    const numeroViaje = document.getElementById('edit_numero_viaje')?.value;
    const centroCosto = document.getElementById('edit_centro_costo')?.value;
    
    console.log('confirmarEliminar - numeroViaje:', numeroViaje, 'centroCosto:', centroCosto);
    
    if (!numeroViaje || !centroCosto) {
        mostrarModalInfo(
            'ERROR',
            'No se pudo obtener el número de viaje o centro de costo. Por favor, intenta nuevamente.',
            'error'
        );
        return;
    }
    
    mostrarModalConfirm(
        `¿Estás seguro de eliminar el viaje ${numeroViaje} - ${centroCosto}? Esta acción eliminará el viaje y todas sus comidas asociadas. No se puede deshacer.`,
        function(confirmado) {
            console.log('Modal confirmación - confirmado:', confirmado);
            if (confirmado) {
                eliminarViaje(numeroViaje, centroCosto);
            }
        }
    );
}

function eliminarViaje(numeroViaje, centroCosto) {
    console.log('eliminarViaje - Enviando:', {numero_viaje: numeroViaje, centro_costo: centroCosto});
    
    fetch('/api/eliminar-viaje', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            numero_viaje: numeroViaje,
            centro_costo: centroCosto
        })
    })
    .then(response => {
        console.log('eliminarViaje - Response status:', response.status);
        return response.json();
    })
    .then(result => {
        console.log('eliminarViaje - Result:', result);
        if (result.success) {
            window.viajeActualizadoExitoso = true;
            mostrarModalInfo(
                'VIAJE ELIMINADO',
                `El viaje ${numeroViaje} ha sido eliminado exitosamente. La página se recargará.`,
                'success'
            );
        } else {
            mostrarModalInfo(
                'ERROR AL ELIMINAR',
                result.message || 'No se pudo eliminar el viaje. Por favor, intenta nuevamente.',
                'error'
            );
        }
    })
    .catch(error => {
        console.error('eliminarViaje - Error:', error);
        mostrarModalInfo(
            'ERROR DE CONEXIÓN',
            'No se pudo conectar con el servidor. Verifica tu conexión e intenta nuevamente.',
            'error'
        );
    });
}

function cancelarEdicion() {
    document.getElementById('buscar_numero_viaje').value = '';
    document.getElementById('paso2-centros').style.display = 'none';
    document.getElementById('paso3-formulario').style.display = 'none';
    document.getElementById('mensaje-busqueda').innerHTML = '';
    document.getElementById('mensaje-resultado-edit').style.display = 'none';
    document.getElementById('paso1-buscar').scrollIntoView({ behavior: 'smooth' });
}

// Cargar administrativos en el select2 del formulario de edición
function cargarAdministrativosEdicion(valorActual) {
    fetch('/api/listar-administrativos')
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            const select = $('#edit_administrativo_responsable');
            select.empty();
            select.append('<option value="">Seleccione un administrativo...</option>');
            result.administrativos.forEach(admin => {
                const selected = admin === valorActual ? 'selected' : '';
                select.append(`<option value="${admin}" ${selected}>${admin}</option>`);
            });
            // Inicializar Select2 después de cargar las opciones
            select.select2({
                placeholder: 'Buscar administrativo...',
                allowClear: true,
                language: {
                    noResults: function() {
                        return "No se encontraron resultados";
                    },
                    searching: function() {
                        return "Buscando...";
                    }
                }
            });
        }
    })
    .catch(error => console.error('Error cargando administrativos:', error));
}

// ==================== FUNCIONES DE MODALES ====================

function mostrarModalInfo(titulo, mensaje, tipo = 'success') {
    const modal = document.getElementById('modalInfo');
    const header = document.getElementById('modalInfoHeader');
    const tituloElem = document.getElementById('modalInfoTitulo');
    const mensajeElem = document.getElementById('modalInfoMensaje');
    
    // Configurar colores según el tipo
    if (tipo === 'success') {
        header.className = 'px-6 py-4 rounded-t-2xl bg-gradient-to-r from-green-500 to-emerald-600';
        tituloElem.innerHTML = `<i class="bi bi-check-circle-fill mr-3 text-3xl"></i>${titulo}`;
    } else if (tipo === 'error') {
        header.className = 'px-6 py-4 rounded-t-2xl bg-gradient-to-r from-red-500 to-red-600';
        tituloElem.innerHTML = `<i class="bi bi-x-circle-fill mr-3 text-3xl"></i>${titulo}`;
    } else if (tipo === 'warning') {
        header.className = 'px-6 py-4 rounded-t-2xl bg-gradient-to-r from-yellow-500 to-orange-600';
        tituloElem.innerHTML = `<i class="bi bi-exclamation-triangle-fill mr-3 text-3xl"></i>${titulo}`;
    } else {
        header.className = 'px-6 py-4 rounded-t-2xl bg-gradient-to-r from-blue-500 to-blue-600';
        tituloElem.innerHTML = `<i class="bi bi-info-circle-fill mr-3 text-3xl"></i>${titulo}`;
    }
    
    mensajeElem.textContent = mensaje;
    modal.classList.remove('hidden');
}

function cerrarModalInfo() {
    const modal = document.getElementById('modalInfo');
    modal.classList.add('hidden');
    
    // Si el modal se cerró después de una actualización exitosa, recargar la página
    if (window.viajeActualizadoExitoso) {
        window.viajeActualizadoExitoso = false;
        location.reload();
    }
}

let accionConfirmadaCallback = null;

function mostrarModalConfirm(mensaje, callback) {
    const modal = document.getElementById('modalConfirm');
    const mensajeElem = document.getElementById('modalConfirmMensaje');
    
    mensajeElem.textContent = mensaje;
    accionConfirmadaCallback = callback;
    modal.classList.remove('hidden');
}

function confirmarAccionModal(confirmado) {
    const modal = document.getElementById('modalConfirm');
    modal.classList.add('hidden');
    
    if (accionConfirmadaCallback) {
        accionConfirmadaCallback(confirmado);
        accionConfirmadaCallback = null;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const inputBuscar = document.getElementById('buscar_numero_viaje');
    if (inputBuscar) {
        inputBuscar.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                buscarCentrosCosto();
            }
        });
    }
});

console.log('editar_viaje.js COMPLETO cargado correctamente');
