# Auditoría de reorientación predictiva M1721

## Dictamen

Se construyó un derivado nuevo de 485 filas y 38 variables, con 79 productos. Es una estructura reproducible de preparación, no un conjunto declarado suficiente para modelización predictiva seria. No se entrenaron modelos ni se hicieron splits.

## Evidencia de partida y alcance

El core histórico contiene 307.183 filas y 24 columnas. La muestra histórica tiene 100 filas y 36 columnas. Se verificaron los cuatro hashes originales y los 1.528 registros de la línea base técnica. La selección v1 parte del core completo, no de la muestra de 100 filas. Se comprobaron por hash las fuentes archivadas consumidas.

La condición es PRODUCT con código exacto presente en una de las 79 fichas OFF válidas. Cada unión valida many_to_one. Se mantuvieron 485 price_id únicos y se comprobó igualdad exacta con el conjunto seleccionable del core. No hubo filtro de moneda, faltantes secundarios ni proof. Las exclusiones de alcance no se suman con sus subcategorías: los siete códigos no encontrados son parte de PRODUCT sin ficha válida, no una categoría adicional independiente.

## Cobertura y posibles refutaciones

Los 485 precios son positivos y tienen fecha, moneda y product_code. Esto es una propiedad observada, no un filtro nuevo. País está presente en 484 filas, ciudad en 479, marcas en 481, categorías OFF en 483 y NOVA en 475. Nutri-Score tiene 432 grados a-e utilizables como tales; sus otros estados requieren tratamiento explícito. Solo 75 filas enlazan con metadatos de proofs archivados; las 410 restantes permanecen.

Las fechas abarcan 2018-03-27 a 2026-09-04. Las diez monedas se conservan separadas. Hay 148 ubicaciones y 14 países, sin coordenadas ni geocodificación añadidas. price_per falta en las 485 filas. Por tanto no puede afirmarse comparabilidad por cantidad/envase. El volumen y la selección heredada no justifican promesas de generalización ni un tamaño mínimo universal.

## Nutrición y decisión de no proyección

Se revisó product.nutrition de las fichas archivadas: 77 de 79 tienen información. Se comprobaron aggregated_set, per, preparation, input_sets, fuente, base original source_per, unidades y presencia de value_computed. Por ejemplo, una ficha combina entradas por porción y por 100 g y valores declarados/calculados; la agregación incluso contiene un valor de nova-group que no debe confundirse con el campo categórico NOVA proyectado. Presencia de una clave no acredita su aptitud.

No se extraen nutrientes numéricos en v1. No se convierte ni promedia información de bases distintas, ni se usa ciegamente nutriments. El reporte nutricion_cobertura_v1.csv documenta presencia por producto, preparación y base; la semántica completa queda pendiente de estudio. La nutrición no es una columna oculta del dataset final.

## Fuga de información y temporalidad

Identidad de producto y marca pueden considerarse relativamente estables solo como hipótesis. Ingredientes, nutrición, categorías y clasificaciones pueden cambiar; no se acredita su estado en cada fecha histórica. off_acquired_at y off_last_modified_t son metadatos de auditoría, no predictores ni prueba de disponibilidad histórica.

price_id, hashes y rutas no son características sustantivas. qc_price_positive y qc_core_eligible dependen de price y se excluyen de candidatos. No se reutiliza qc_core_eligible como elegibilidad predictiva: además exige proof, condición que no debe borrar automáticamente un precio válido. No se publican contenidos de predictions que puedan incluir precio observado. Una futura estrategia de validación debe considerar productos, ubicaciones, fechas y proofs compartidos; aquí no se divide la muestra.

## Preservación y reproducción

Los cuatro datasets y el Notebook histórico permanecen intactos. El nuevo Notebook contiene explicaciones y resultados de v1, además de evidencia histórica SQL/NoSQL identificada como tal. La selección y extracción se ejecutaron sobre el archivo privado autorizado. La reproducción pública empieza en tres proyecciones mínimas incluidas, no en los originales excluidos. Los dos hashes nuevos están en data/manifests/version_v1.json.

## Decisiones

D1: derivado v1 sin reemplazar históricos. D2: selección de todas las filas enriquecibles, sin filtro secundario. D3: year, month y day_of_week desde date; no quarter redundante. D4: nutrición no proyectada por cautela semántica. D5: JSON crudos y todas las imágenes fuera del paquete público. D6: comparación monetaria y splits pendientes de estudio. D7: no modelo, no OCR, no Spark y no nuevas adquisiciones. D8: publicación y licencia del código propio pendientes de decisión humana.

## Antecedente de presentación

El FAIL del borde decorativo del DOCX anterior pertenece a esa entrega histórica. No se modificó ni se declara resuelto por esta reorientación; esta orden produce Notebook, HTML, datos y documentación nueva, no un PDF/DOCX revisado.
