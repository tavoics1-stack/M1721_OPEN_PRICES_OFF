# Diccionario versionado del dataset v1

Una fila es una observación price_id. CSV conserva códigos como texto y nulos como campos vacíos. Parquet conserva tipos anulables y precio Decimal, sin conversión monetaria. La matriz adjunta contiene roles, cobertura, riesgos y preparación.

| Variable | Fuente | Tipo | Presencia | Uso y preparación |
|---|---|---|---|---|
| price_id | OP.id | Int64 | 485/485 filas | Identidad de observación; no predictor. No codificar como magnitud |
| price_type | OP.type | string | 485/485 filas | Alcance PRODUCT constante. Separar PRODUCT de CATEGORY |
| product_code | OP.product_code = OFF.product.code | string | 485/485 filas | Clave exacta de producto; candidato categórico solo con justificación posterior. Conservar ceros; no tratar como número continuo |
| category_tag | OP.category_tag | string | 0/485 filas | Taxón CATEGORY; no aplica en v1 PRODUCT. No sustituir categories_tags OFF |
| price | OP.price | object | 485/485 filas | Importe observado en currency. Delimitar moneda, cantidad y envase |
| price_per | OP.price_per | string | 0/485 filas | Base de medida del precio. No imputar unidad; ausente en PRODUCT |
| currency | OP.currency | string | 485/485 filas | Definir escala y estrato monetario. Una moneda o estrategia posterior justificada |
| date | OP.date | string | 485/485 filas | Fecha de observación. Conservar original y validar formato |
| location_id | OP.location_id | Int64 | 485/485 filas | Clave de ubicación; candidato categórico condicionado. No magnitud continua; prever lugares nuevos |
| proof_id | OP.proof_id/proof_type | Int64 | 485/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
| proof_type | OP.proof_id/proof_type | string | 485/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
| country | OP.location_osm_address_country | string | 484/485 filas | País del registro. Normalizar etiquetas; no geocodificar ni imputar |
| city | OP.location_osm_address_city | string | 479/485 filas | Ciudad del registro. Normalizar con país; tratar faltantes |
| qc_price_positive | OP y QC histórico | boolean | 485/485 filas | Control de calidad; excluir de predictores. No convertir qc_core_eligible en regla de modelado |
| qc_currency_present | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_date_present | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_date_not_future | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_date_valid | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_proof_present | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_proof_visual | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_product_identity | OP y QC histórico | boolean | 485/485 filas | Control de calidad, no predictor automático. Conservar flag; definir política específica después |
| qc_core_eligible | OP y QC histórico | boolean | 485/485 filas | Control de calidad; excluir de predictores. No convertir qc_core_eligible en regla de modelado |
| product_name | OFF.product.product_name | string | 485/485 filas | Nombre comercial. No codificar texto automáticamente |
| brands | OFF.product.brands | string | 481/485 filas | Marcas declaradas. Normalizar listas, duplicados y faltantes |
| categories_tags | OFF.product.categories_tags | string | 483/485 filas | Lista de taxones OFF serializada como JSON. Parsear lista; definir codificación posterior |
| nutriscore_grade | OFF.product.nutriscore_grade | string | 485/485 filas | Grado a-e o estado informativo. Separar unknown/not-applicable de grados válidos |
| nova_group | OFF.product.nova_group | string | 475/485 filas | Grupo de procesamiento. Validar dominio 1-4; representar como categoría |
| off_source_sha256 | Catálogo fuente OFF | string | 485/485 filas | Huella de origen. Excluir de predictores |
| off_acquired_at | Catálogo OFF.acquired_at | string | 485/485 filas | Momento de captura de ficha. Metadato UTC, no fecha del precio |
| off_last_modified_t | OFF.product.last_modified_t | Int64 | 485/485 filas | Metadato de versión. Convertir UTC solo para auditoría; no predictor |
| off_history_status | Decisión metodológica v1 | string | 485/485 filas | NO_VERIFICABLE_HISTORICAMENTE. No usar como predictor; constante |
| proof_metadata_sha256 | OP API proof metadata (proyección) | string | 75/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
| proof_metadata_type | OP API proof metadata (proyección) | string | 75/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
| proof_prediction_count | OP API proof metadata (proyección) | Int64 | 75/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
| year | Derivación de date | Int64 | 485/485 filas | Año de observación. Entero; derivación sin consultar futuro |
| month | Derivación de date | Int64 | 485/485 filas | Mes 1-12. Categoría temporal; codificación posterior |
| day_of_week | Derivación de date | Int64 | 485/485 filas | Día de semana: lunes 0, domingo 6. Categoría temporal; codificación posterior |
| proof_metadata_available | OP API proof metadata (proyección) | boolean | 485/485 filas | Evidencia y trazabilidad; no predictor. Nulo es no consultado; False no implica inexistencia |
