-- Reporte de Facturación por Rango de Fechas
-- Datos para facturación con guía de activos
-- Parámetros: fecha_inicio, fecha_fin
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
    pallets_pl_negro_alternativo,
    guia_1 AS "Guia_activos"
FROM viajes
WHERE fecha BETWEEN ? AND ?
ORDER BY fecha, numero_viaje
