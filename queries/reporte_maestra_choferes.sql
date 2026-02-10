-- Reporte de Maestra de Choferes (Conductores)
-- Lista completa de todos los conductores con nombres, RUT y teléfonos
-- Sin parámetros requeridos
-- Ordenado por nombre ascendente

SELECT 
    nombre,
    rut,
    celular
FROM maestras_choferes
ORDER BY nombre ASC
