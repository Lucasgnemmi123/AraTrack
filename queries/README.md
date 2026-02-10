# Queries SQL para Reportes

Este directorio contiene las queries SQL utilizadas en los reportes de Excel.

## Estructura

Cada archivo `.sql` contiene:
- Comentarios descriptivos del reporte
- Parámetros esperados
- Query SQL con placeholders (?)
- Ordenamiento de resultados

## Archivos Disponibles

### `reporte_maestra_casinos.sql`
- **Descripción**: Reporte completo de centros de costo (casinos)
- **Parámetros**: Ninguno
- **Columnas retornadas**: 3 columnas (codigo_costo, casino, ruta)
- **Ordenamiento**: Por código de costo ascendente
- **Usado en**: `/api/descargar-reporte-casinos`

### `reporte_maestra_choferes.sql`
- **Descripción**: Reporte completo de conductores (choferes)
- **Parámetros**: Ninguno
- **Columnas retornadas**: 3 columnas (nombre, rut, celular)
- **Ordenamiento**: Por nombre ascendente
- **Usado en**: `/api/descargar-reporte-choferes`

### `reporte_comidas_implementos.sql`
- **Descripción**: Reporte de comidas e implementos filtrado por rango de fechas
- **Parámetros**: 
  - `?` (posición 1): fecha_inicio (formato: 'YYYY-MM-DD')
  - `?` (posición 2): fecha_fin (formato: 'YYYY-MM-DD')
- **Columnas retornadas**: 10 columnas (fecha, numero_viaje, casino, conductor, numero_centro_costo, guia_comida, descripcion, kilo, bultos, proveedor)
- **Ordenamiento**: Por fecha y número de viaje
- **Usado en**: `/api/descargar-reporte-comidas`

### `reporte_viajes_completos.sql`
- **Descripción**: Reporte completo de viajes con todos los campos
- **Parámetros**: 
  - `?` (posición 1): fecha_inicio (formato: 'YYYY-MM-DD')
  - `?` (posición 2): fecha_fin (formato: 'YYYY-MM-DD')
- **Columnas retornadas**: 63 columnas (todos los campos de la tabla viajes)
- **Ordenamiento**: Por fecha y número de viaje
- **Usado en**: `/api/descargar-reporte-viajes`

### `reporte_facturacion.sql`
- **Descripción**: Reporte de facturación con guías concatenadas
- **Parámetros**: 
  - `?` (posición 1): fecha_inicio (formato: 'YYYY-MM-DD')
  - `?` (posición 2): fecha_fin (formato: 'YYYY-MM-DD')
- **Columnas retornadas**: 11 columnas (numero_viaje, casino, costo_codigo, fecha, num_wencos, bin, pallets, pallets_chep, pallets_pl_negro_grueso, pallets_pl_negro_alternativo, guias_concatenadas)
- **Ordenamiento**: Por fecha y número de viaje
- **Usado en**: `/api/descargar-reporte-facturacion`

## Convenciones

1. **Nombres de archivo**: `reporte_[nombre_descriptivo].sql`
2. **Comentarios**: Incluir descripción, parámetros y formato esperado
3. **Placeholders**: Usar `?` para parámetros (SQLite3)
4. **Ordenamiento**: Incluir ORDER BY para resultados consistentes
5. **Formato**: Indentación de 4 espacios, SQL keywords en MAYÚSCULAS

## Agregar Nuevas Queries

Para agregar un nuevo reporte:

1. Crear archivo `queries/reporte_[nombre].sql`
2. Documentar parámetros en comentarios
3. Escribir query con placeholders
4. Actualizar este README
5. Implementar endpoint en `app_web.py` usando `cargar_query()`
