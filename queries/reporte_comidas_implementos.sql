-- Reporte de Comidas e Implementos por Rango de Fechas
-- Cruza la tabla comidas_preparadas con viajes para obtener información de fecha
-- Parámetros: fecha_inicio, fecha_fin
-- Formato esperado: 'YYYY-MM-DD'

SELECT 
    v.fecha,
    v.numero_viaje,
    v.casino,
    v.conductor,
    c.numero_centro_costo,
    c.guia_comida,
    c.descripcion,
    c.kilo,
    c.bultos,
    c.proveedor
FROM comidas_preparadas c
INNER JOIN viajes v 
    ON c.numero_viaje = v.numero_viaje 
    AND c.numero_centro_costo = v.costo_codigo
WHERE v.fecha BETWEEN ? AND ?
ORDER BY v.fecha, v.numero_viaje
