# Dataset integrado de precios y productos para preparación predictiva

## Contexto documental actualizado al 2026-09-12

El Notebook incluido en notebooks/ es el técnico v1: 36 celdas totales y 14 de código. outputs/notebook_execution_v1.json corresponde a ese Notebook. El Notebook académico final, entregado por separado en 02_NOTEBOOK_MAESTRO de M1721_ENTREGA_FINAL_REORIENTADA, tiene 128 celdas totales y 46 de código; no está incluido en este ZIP.

Las 170 referencias de data/manifests/fuentes_v1.csv corresponden al manifiesto público v1. Las 259 fuentes corresponden al inventario histórico privado, no al contenido redistribuido. La verificación posterior en Docker registró PostgreSQL 17.11 y MongoDB 8.3.9 con mongo:8; MongoDB 8.0.29 corresponde a la ejecución histórica portable y sus registros se conservan.

Las seis capturas PG-1, PG-2, PG-3, MG-1, MG-2 y MG-3 ya fueron realizadas. Están incorporadas en Evidencia_Visual_PostgreSQL_MongoDB_M1721.docx, dentro de 05_EVIDENCIA_VISUAL_BD de la entrega académica, fuera de este ZIP. Su ausencia aquí no significa que estén pendientes ni impide reconstruir v1 desde las proyecciones públicas. La guía docs/GUIA_CAPTURAS_PGADMIN_COMPASS.md identifica esa evidencia. No se añaden imágenes a este paquete.


Grupo 2. M1721, ESPOCH.

La información para estudiar precios está distribuida entre observaciones de Open Prices, fichas de Open Food Facts y evidencias relacionadas. Este trabajo reúne esos datos sin perder la identidad de cada observación y documenta qué podría utilizarse en una futura regresión del precio.

## Objetivo y alcance

Construir un dataset integrado, trazable y reproducible a partir de Open Prices y Open Food Facts, que reúna información sobre precios, características de los productos, ubicación y momento del registro, y que quede preparado como base para el posterior desarrollo de modelos predictivos del precio de productos alimenticios.

Pregunta central: ¿Cómo integrar de forma trazable y reproducible los datos de Open Prices y Open Food Facts para construir un dataset que reúna el precio, las características del producto, la ubicación y el momento del registro, y que sirva como base para el desarrollo posterior de un modelo de predicción de precios?

Pregunta predictiva futura: ¿En qué medida las características del producto, la ubicación y el momento del registro permiten predecir el precio de un producto alimenticio?

La construcción, integración, documentación y validación del dataset están realizadas. La pregunta predictiva corresponde a una etapa posterior: el modelo no ha sido entrenado ni evaluado y todavía no se ha demostrado suficiencia ni rendimiento predictivo del dataset.

Este proyecto construye y documenta el conjunto de datos necesario para una futura tarea de predicción de precios; el entrenamiento y evaluación del modelo quedan fuera del alcance de esta entrega.

El resultado actual materializa una estructura de preparación, no demuestra que su tamaño, cobertura o comparabilidad sean suficientes para una modelización seria. No se entrenaron modelos, dividieron datos, evaluaron algoritmos, aplicaron OCR ni convirtieron monedas. Tampoco se estudian inflación, causalidad ni forecasting.

## Resultado final del proyecto

Se construyó `precios_productos_predictive_preparation_v1`, con **485 observaciones y 38 variables**, en CSV y Parquet dentro de `data/processed/`. Son dos formatos del mismo conjunto. La unidad es una observación de precio identificada por `price_id`; los 485 identificadores son únicos.

| Dataset | Dimensiones | Función y distribución |
|---|---|---|
| open_prices_core_curated | 307.183 × 24 | Core histórico completo del snapshot. Preservado en archivo privado, sin cambios. |
| precios_productos_multifuente_curated | 100 × 36 | Demostración histórica de integración, intencional y no representativa. Preservada sin cambios. |
| precios_productos_predictive_preparation_v1 | 485 × 38 | Todas las observaciones PRODUCT del core que pueden enriquecerse con las 79 fichas OFF válidas archivadas. Incluido aquí. |

La selección de v1 no exige proof, ciudad, nutrición, marca ni un valor de calidad específico. Los no encontrados y CATEGORY siguen en los históricos; no pertenecen al alcance PRODUCT con OFF válido de este derivado. Se documentan los conteos y motivos de exclusión. La selección hereda el sesgo de los códigos OFF disponibles y no constituye una muestra representativa.

## Fuentes y arquitectura

Open Prices aporta precios, fechas, monedas, ubicaciones y relaciones con proofs. El origen fijado es la revisión `e3cf81a0a08d3875a43c22f79ea6afce716e92f9`, con fecha de snapshot 2026-09-05. Open Food Facts aporta atributos de producto: se conservan privadamente 86 respuestas completas, de las cuales 79 contienen producto válido. Se utilizan las ya archivadas, sin llamadas nuevas. Las 83 imágenes privadas no se redistribuyen.

Los originales se conservaron antes de transformar y se verificaron por hash. PostgreSQL organizó entidades y relaciones estables; MongoDB conservó respuestas OFF completas. Python realizó validación e integración. Los archivos visuales tuvieron una función de evidencia, no de predictor. No todos los proofs son imágenes ni todos sus metadatos fueron adquiridos.

La integración usa códigos exactos y uniones `many_to_one`, sin coincidencias por nombre. Primero se seleccionan del core las filas PRODUCT con una ficha OFF válida; después se enriquecen con OFF y se agregan los metadatos de proof disponibles por `proof_id`. Cada unión conserva 485 filas.

## Variables y cobertura

Precio, código de producto, fecha, moneda y ubicación están presentes en las 485 filas. Hay 79 productos, 148 ubicaciones y 14 países; falta país en una fila y ciudad en seis. Marca está presente en 481 filas, categorías OFF en 483 y NOVA en 475. Nutri-Score conserva también estados desconocidos y no aplicables; no deben interpretarse como grados a–e.

`year`, `month` y `day_of_week` se derivan exclusivamente de la fecha original. Lunes se codifica como 0 y domingo como 6. Se conserva `date`. `location_id` es un identificador categórico, no una magnitud continua. No se inventaron coordenadas ni geocodificación. El dataset no incorpora una variable de tienda; país y ciudad no equivalen a tienda.

Hay metadatos de proof archivados para 75 observaciones. Las otras 410 permanecen con esos campos nulos: no se interpreta desconocido como cero. Las predictions son del proveedor; solo se conserva su conteo, sin contenido que pueda reproducir el precio o datos de recibos.

## Preparación para una futura predicción de precios

`price` sería la variable objetivo potencial. Marca, categorías, atributos seleccionados del producto, país, ciudad y componentes de la fecha son candidatos, sujetos a preparación y validación. Nombre y código tienen funciones descriptivas o de identificación; no deben incorporarse automáticamente como variables numéricas. La matriz de variables explica el tratamiento de cada campo.

Las 485 observaciones abarcan 2018-03-27 a 2026-09-04 y diez monedas: 449 EUR, 23 USD, cuatro GBP, dos AED, dos INR y una de cada una de ARS, ADP, AMD, THB y AFN. Una futura tarea debe delimitar una moneda o justificar otra estrategia. Conservar un código monetario no certifica su coherencia histórica. No se realizó conversión ni se eliminaron monedas.

`price_per` está ausente en todas las filas PRODUCT de v1. Falta resolver comparabilidad de cantidad y envase. Las fichas OFF capturadas no acreditan el estado de cada producto en cada fecha histórica. Marca e identidad pueden ser relativamente estables, pero no están verificadas históricamente; ingredientes, composición y clasificaciones pueden cambiar.

La nutrición existe en `product.nutrition` de 77 productos archivados. No se proyecta en v1: hay bases de medida, preparación, fuentes y valores calculados que requieren una validación específica. El campo legado `nutriments` no sustituye esa revisión. Los ingredientes libres y las cantidades de envase tampoco se proyectaron en esta versión.

No se proponen como predictores `price_id`, hashes, rutas, metadatos administrativos, `qc_price_positive` ni `qc_core_eligible`. Los últimos dependen del objetivo. Los campos de proof se conservan para trazabilidad, no como información disponible antes de observar el precio. Un estudio posterior deberá evitar agregaciones con futuro y evaluar dependencias entre productos, ubicaciones, fechas y proofs antes de elegir una separación de entrenamiento y evaluación. Aquí no se hizo ningún split.

## Estructura y reproducción

`data/inputs/` contiene tres proyecciones mínimas redistribuibles de core, OFF y proofs. **No son los originales crudos**. `data/processed/` contiene el resultado v1; `data/manifests/` registra fuentes, hashes y linaje. `src/` contiene la reconstrucción pública; `notebooks/`, el nuevo Notebook y su HTML. `docs/` reúne auditoría, matriz, diccionario y decisiones. `outputs/` conserva controles y evidencia resumida. `sql/` y `mongodb/` contienen recursos históricos, no motores ni bases cargadas.

Se probó Python 3.12.14, pandas 3.0.1 y pyarrow 25.0.1. Preparar previamente un entorno con `requirements.txt`. No se incluyen intérpretes ni paquetes. Activar ese entorno y ejecutar `reproducir.bat` desde esta carpeta. En otros sistemas puede usarse `python -B src/reproducir.py`. La ejecución no instala, no descarga ni inicia bases de datos. Puede indicarse un intérprete ya instalado con la variable de entorno `M1721_PYTHON`.

El pipeline comprueba hashes de las tres proyecciones, vuelve a integrar, deriva fechas y escribe CSV/Parquet temporales. Compara los dos hashes reconstruidos con `data/manifests/version_v1.json` y con los archivos entregados. No sobrescribe los finales. Se requiere la misma familia de versiones para esperar identidad binaria de Parquet. El entorno de dependencias debe estar disponible antes de trabajar offline.

El nuevo Notebook puede ejecutarse desde esta carpeta o desde `notebooks/`. Explica y comprueba v1 con los insumos redistribuidos y presenta SQL/MongoDB como evidencia histórica, no como consultas en vivo. El Notebook Maestro anterior permanece intacto en el archivo privado; su comprobación original de 259 fuentes no puede repetirse desde esta copia.

La reproducción pública **solo reconstruye v1 desde las proyecciones incluidas**. No reproduce la adquisición, la selección desde el core completo, las cuatro salidas históricas ni los originales excluidos. Esas operaciones se verificaron en el entorno privado autorizado. Una nueva descarga oficial podría contener otros datos y no recuperar los hashes históricos. Los hashes y URLs del manifiesto permiten identificar los insumos exactos necesarios para una reproducción privada completa.

## Privacidad, licencias y publicación

No se incluyen imágenes, JSON OFF completos, identidades de contribuidores, contactos, texto completo de predictions, rutas personales, secretos, entornos ni estados de bases. Los campos de producto incluidos se revisaron como nombres comerciales, marcas y taxones. Las exclusiones y el alcance de esta revisión están en `docs/PRIVACIDAD_Y_REDISTRIBUCION.md`.

La nota `LICENCIAS_Y_ATRIBUCION.md` separa datos de terceros y código. Se mantiene atribución a Open Prices, Open Food Facts y sus contribuyentes. La documentación archivada indica ODbL para bases y DbCL para contenidos OFF; no se inventa una licencia única que cubra todo. La publicación y la elección de licencia del código propio quedan pendientes de autorización del titular. No se hizo push ni se creó un repositorio remoto.

## Referencias

[Datos de Open Prices](https://openfoodfacts.github.io/open-prices/guides/data/), [snapshot fijado](https://huggingface.co/datasets/openfoodfacts/open-prices/tree/e3cf81a0a08d3875a43c22f79ea6afce716e92f9), [API Open Food Facts](https://openfoodfacts.github.io/openfoodfacts-server/api/), [términos Open Food Facts](https://world.openfoodfacts.org/terms-of-use). Se usaron las fuentes y copias documentales previamente archivadas; no se hizo consulta nueva en esta versión.


## Modelo de bases de datos

PostgreSQL organiza precios, productos, categorías, ubicaciones y proofs mediante claves primarias, cuatro FK y el CHECK PRODUCT/CATEGORY. MongoDB conserva fichas OFF con objetos y listas anidadas. Docker reproduce ambos motores; Python comprueba la integración por código exacto sin multiplicar price_id.

El ERD y los modelos están en `docs/diagramas`. Las consultas de lectura están en `sql/consultas_demostrativas_m1721.sql` y `nosql/consultas_mongodb_m1721.js`; sus resultados sanitizados están en `outputs/evidencia_bd`. Compose y su guía están en `infra/docker`. Las cargas explícitas están en `src/db/ejecutar_bd.py` y la comprobación de las 38 columnas en `src/db/validar_integracion.py`.

LOCAL_FULL utiliza los originales privados del maestro. PUBLIC_DEMO utiliza únicamente las proyecciones incluidas, en la base separada m1721_public_demo: 485 precios, 79 productos y 79 fichas proyectadas. No reproduce los 307.183 precios ni las 86 respuestas completas. Siga README_DOCKER.md para configurar un .env local que nunca debe publicarse. No se distribuyen imágenes privadas, JSON completos, secretos ni volúmenes.

Las evidencias v1 anteriores permanecen como registros históricos de su ejecución. El README se amplió en este empaquetado; por eso MANIFEST_V1.csv y SHA256SUMS.txt describen la versión previa, no toda esta ampliación. Los controles vigentes del paquete son MANIFEST_EMPAQUETADO.csv y SHA256SUMS_EMPAQUETADO.txt. El mecanismo reproducir.bat y los hashes canónicos no cambian.


---

## Contribución — Wilson Andrés Sani

**Rama:** `feature/wilsonandressani-cyber`

En el proyecto de integración de datos de Open Prices y Open Food Facts para la preparación de un dataset orientado a la futura predicción de precios de productos alimenticios. Esta contribución documenta la revisión del flujo de trabajo con Git y GitHub (ramas, commits y sincronización) aplicado sobre el repositorio compartido del equipo, verificando la estructura del dataset final (precios_productos_predictive_preparation_v1) y la organización de las carpetas del proyecto (data, docs, notebooks, sql, mongodb, infra/docker).
*Wilson Andrés Sani*
