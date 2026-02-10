-- Reporte de Maestra de Casinos (Centros de Costo)
-- Lista completa de todos los centros de costo con sus códigos, nombres y rutas
-- Sin parámetros requeridos
-- Ordenado por código de costo ascendente

SELECT 
    codigo_costo,
    casino,
    ruta
FROM maestras_casinos
ORDER BY codigo_costo ASC
