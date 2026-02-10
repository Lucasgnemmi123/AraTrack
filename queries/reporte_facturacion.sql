-- Reporte de Facturación por Rango de Fechas
-- Datos para facturación con guías concatenadas
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
    TRIM(
        COALESCE(guia_1, '') || ' ' ||
        COALESCE(guia_2, '') || ' ' ||
        COALESCE(guia_3, '') || ' ' ||
        COALESCE(guia_4, '') || ' ' ||
        COALESCE(guia_5, '') || ' ' ||
        COALESCE(guia_6, '') || ' ' ||
        COALESCE(guia_7, '') || ' ' ||
        COALESCE(guia_8, '') || ' ' ||
        COALESCE(guia_9, '') || ' ' ||
        COALESCE(guia_10, '') || ' ' ||
        COALESCE(guia_11, '') || ' ' ||
        COALESCE(guia_12, '') || ' ' ||
        COALESCE(guia_13, '') || ' ' ||
        COALESCE(guia_14, '')
    ) AS guias_concatenadas
FROM viajes
WHERE fecha BETWEEN ? AND ?
ORDER BY fecha, numero_viaje
