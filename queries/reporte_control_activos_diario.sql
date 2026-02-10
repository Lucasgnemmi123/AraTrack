-- Reporte de Control de Activos Diario
-- Datos de control de activos para un día específico
-- Parámetros: fecha (un solo día)
-- Formato esperado: 'YYYY-MM-DD'

SELECT 
    numero_viaje,
    casino,
    costo_codigo,
    fecha,
    num_wencos,
    bin,
    pallets,
    pallets_chep,
    pallets_pl_negro_grueso,
    pallets_pl_negro_alternativo
FROM viajes
WHERE fecha = ?
ORDER BY numero_viaje
