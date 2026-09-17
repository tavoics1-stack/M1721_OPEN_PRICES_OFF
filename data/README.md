# Datos de v1

inputs contiene proyecciones derivadas permitidas, no fuentes crudas: core_enriquecible_v1.csv (485 filas), off_proyeccion_v1.csv (79 códigos únicos) y proofs_proyeccion_v1.csv (83 ids únicos). Se conservaron nombres comerciales y taxones revisados; no autores de contribuciones ni imágenes. La reproducción pública no afirma haber leído los originales privados.

processed contiene precios_productos_predictive_preparation_v1.csv y .parquet, ambos 485 × 38. Son dos formatos equivalentes. Al leer CSV, especificar product_code como texto para conservar ceros iniciales. price expresa importe en currency, no una moneda común ni necesariamente precio por unidad. Identificadores no son magnitudes continuas. Nulo no equivale a cero.

manifests contiene fuentes con URLs/hashes/fechas, versión, linaje por price_id, exclusiones de alcance y exclusiones de imágenes. La fuente OP está fijada a una revisión; una nueva consulta OFF no garantiza recuperar la misma ficha. La reproducción completa de originales requiere archivos exactos autorizados y no está cubierta por esta copia pública.
