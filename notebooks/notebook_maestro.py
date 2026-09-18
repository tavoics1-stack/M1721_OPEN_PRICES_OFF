# %% [markdown]
# # Dataset integrado de precios y productos para preparación predictiva
# 
# Grupo 2. M1721, ESPOCH. Versión académica v1. El Notebook histórico permanece intacto. Esta versión trabaja con proyecciones redistribuibles y conserva la diferencia entre reproducción pública y archivo privado.

# %% [markdown]
# ## Problema, finalidad y alcance
# 
# Los precios, características del producto y evidencias están distribuidos entre fuentes heterogéneas. La finalidad posterior es una regresión del precio. El alcance actual termina en construir y documentar el dataset; no en entrenar o evaluar modelos.
# 
# Construir un dataset integrado, trazable y reproducible a partir de Open Prices y Open Food Facts, que reúna información sobre precios, características de los productos, ubicación y momento del registro, y que quede preparado como base para el posterior desarrollo de modelos predictivos del precio de productos alimenticios.

# %%
from pathlib import Path
import sys, json, hashlib
import pandas as pd
from IPython.display import display
ROOT = Path.cwd()
if not (ROOT / 'data/manifests/version_v1.json').is_file():
    ROOT = ROOT.parent
assert (ROOT / 'data/manifests/version_v1.json').is_file(), 'Ejecutar desde la raíz o notebooks/'
sys.path.insert(0, str(ROOT / 'src'))
import reproducir as pipeline
pipeline.block_network()
version = json.loads((ROOT / 'data/manifests/version_v1.json').read_text(encoding='utf-8'))
display(pd.DataFrame([{'Python':sys.version.split()[0], 'pandas':pd.__version__, 'modo':'OFFLINE_DESDE_PROYECCIONES'}]))

# %% [markdown]
# ## Fuentes, adquisición, formatos y metadatos
# 
# El archivo privado conserva el Parquet OP fijado, 86 respuestas OFF completas y 83 metadatos de proofs. Se verificaron sus hashes antes de proyectar. No se adquirieron nuevas fuentes. La copia pública contiene proyecciones CSV y el resultado CSV/Parquet; no los originales crudos.
# 
# El manifiesto permite identificar fuente, adquisición, revisión y hash. No debe confundirse la fecha de adquisición con la fecha del precio.

# %%
sources = pd.read_csv(ROOT/'data/manifests/fuentes_v1.csv', dtype='string')
display(sources[['ruta_original','adquirido_utc','snapshot','sha256']].head(6))
display(pd.DataFrame([{'originales_identificados':len(sources),'verificacion_original_publica':'No: originales excluidos por privacidad'}]))

# %% [markdown]
# Los hashes identifican archivos; no prueban exactitud del contenido ni disponibilidad histórica del atributo. Los originales fueron preservados antes de transformar. La construcción privada produjo proyecciones explícitas y no se presenta esa selección como adquisición original pública.

# %% [markdown]
# ## Arquitectura SQL, NoSQL y archivos
# 
# Open Prices es el núcleo estructurado. PostgreSQL organiza productos, categorías, precios, ubicaciones y proofs mediante claves. MongoDB conserva fichas OFF como documentos completos con objetos y listas. Los proofs son entidades de evidencia; no todos son fotografías. Las imágenes seleccionadas permanecen privadas. Python hace la integración, no un JOIN entre motores.

# %%
pg = json.loads((ROOT/'outputs/postgresql_execution.json').read_text(encoding='utf-8'))
mongo = json.loads((ROOT/'outputs/mongodb_execution.json').read_text(encoding='utf-8'))
display(pd.DataFrame(pg['checks']))
display(pd.DataFrame([{'motor':'MongoDB','version':mongo['version'],'documentos':mongo['documents'],'consultas':mongo['queries'],'indices':len(mongo['indexes'])}]))

# %% [markdown]
# Estos resultados son evidencia histórica de ejecución, no consultas actuales. PostgreSQL verificó una vista de 307.183 observaciones y MongoDB conservó 86 respuestas. Los scripts SQL y recursos MongoDB se incluyen para explicar el diseño histórico; requieren insumos privados y no se ejecutan aquí.

# %% [markdown]
# ## Integración y cardinalidades
# 
# En la ejecución privada se seleccionaron del core todas las observaciones PRODUCT cuyo código coincide exactamente con una ficha OFF válida. No se filtró por moneda, ciudad, nutrición o proof. Aquí reconstruimos la integración desde esas proyecciones, comprobando unicidad de cada clave antes de unir.

# %%
core = pd.read_csv(ROOT/'data/inputs/core_enriquecible_v1.csv', dtype='string')
off = pd.read_csv(ROOT/'data/inputs/off_proyeccion_v1.csv', dtype='string')
proof = pd.read_csv(ROOT/'data/inputs/proofs_proyeccion_v1.csv', dtype='string')
assert core.price_id.is_unique and off.product_code.is_unique and proof.proof_id.is_unique
a = core.merge(off, on='product_code', how='left', validate='many_to_one')
b = a.merge(proof, on='proof_id', how='left', validate='many_to_one')
assert len(core) == len(a) == len(b) and b.price_id.is_unique
display(pd.DataFrame({'etapa':['selección core','unión OFF','unión proof'],'filas':[len(core),len(a),len(b)]}))

# %% [markdown]
# Las uniones conservan 485 observaciones. La ausencia de metadatos secundarios no multiplica ni elimina precios. Los siete productos OFF no encontrados y las observaciones CATEGORY permanecen en los datasets históricos; el nuevo alcance exige una ficha válida, no modifica esos históricos.

# %%
d = pipeline.build(ROOT)
assert d.price_id.is_unique and d.price_type.eq('PRODUCT').all()
display(d[['price_id','product_code','price','currency','date','country','city','product_name']].head(8))

# %% [markdown]
# ## Resultado final del proyecto
# 
# El resultado nuevo es precios_productos_predictive_preparation_v1. El core conserva el snapshot completo; el multifuente histórico demuestra integración; v1 materializa todas las filas actualmente enriquecibles con OFF archivado y deriva componentes temporales. Ninguno se presenta como prueba de suficiencia predictiva.

# %%
display(pd.DataFrame([
    {'dataset':'open_prices_core_curated','filas':307183,'columnas':24,'rol':'Histórico completo, privado e intacto'},
    {'dataset':'precios_productos_multifuente_curated','filas':100,'columnas':36,'rol':'Demostración histórica, privada e intacta'},
    {'dataset':pipeline.NAME,'filas':len(d),'columnas':len(d.columns),'rol':'Preparación v1 incluida'}]))
display(pd.DataFrame({'variable':d.columns,'presentes':d.notna().sum().values,'tipo':d.dtypes.astype(str).values}))

# %% [markdown]
# ## Calidad, faltantes y evidencia
# 
# Los flags históricos se conservan sin modificar su definición. qc_core_eligible incluye proof y depende del precio: no es una regla automática para seleccionar datos predictivos. Los nulos de metadatos indican información no archivada, no ausencia de evidencia en origen.

# %%
display(pd.DataFrame([{'flag':c,'false':int((~d[c]).sum())} for c in d if c.startswith('qc_')]))
display(pd.DataFrame([{'metadatos_proof_presentes':int(d.proof_metadata_available.sum()),'sin_metadatos_archivados':int((~d.proof_metadata_available).sum()),'filas_conservadas':len(d)}]))
display(d.nutriscore_grade.value_counts(dropna=False).rename_axis('estado').to_frame('filas'))

# %% [markdown]
# Las 410 filas sin metadatos archivados permanecen. Un estado unknown o not-applicable de Nutri-Score no es un grado a-e. No se imputaron faltantes ni se eliminaron observaciones secundariamente.

# %% [markdown]
# ## Preparación del dataset para una futura predicción de precios
# 
# price sería el objetivo potencial. Marca, categorías OFF, atributos seleccionables de producto, lugar y fecha son candidatos condicionados. Los identificadores se conservan para trazabilidad y no se tratan como números continuos. La matriz diferencia candidatos, descriptores, identificadores, riesgos de leakage y variables que necesitan preparación.

# %%
matrix = pd.read_csv(ROOT/'docs/MATRIZ_VARIABLES_PARA_FUTURO_MODELADO.csv')
display(matrix[['VARIABLE','COBERTURA','CLASIFICACION','PREPARACION_NECESARIA']])

# %% [markdown]
# ## Variables temporales y disponibilidad histórica
# 
# year, month y day_of_week derivan solo de date; lunes es 0. No se añadió quarter redundante. Los metadatos de captura OFF son distintos de la fecha del precio. Marca e identidad relativamente estables siguen sin certificación histórica; categorías, ingredientes, nutrición y clasificaciones pueden cambiar.

# %%
dates = pd.to_datetime(d.date)
assert d.year.eq(dates.dt.year).all()
assert d.month.eq(dates.dt.month).all()
assert d.day_of_week.eq(dates.dt.dayofweek).all()
display(d[['date','year','month','day_of_week','off_acquired_at','off_history_status']].head())

# %% [markdown]
# ## Moneda, ubicación y comparabilidad
# 
# Se conserva currency. Una futura tarea deberá trabajar dentro de una moneda o justificar otra estrategia posteriormente. No hubo conversión. price_per está ausente en PRODUCT; falta resolver cantidad/envase. location_id es categórico; país y ciudad no representan coordenadas ni una tienda identificada por nombre.

# %%
display(d.groupby('currency').agg(filas=('price_id','size'),productos=('product_code','nunique')))
display(pd.DataFrame([{'price_per_presentes':int(d.price_per.notna().sum()),'paises':d.country.nunique(),'ubicaciones':d.location_id.nunique(),'pais_nulo':int(d.country.isna().sum()),'ciudad_nula':int(d.city.isna().sum())}]))

# %% [markdown]
# ## Información nutricional
# 
# Se revisaron 79 fichas: 77 contienen nutrition. La estructura distingue bases y preparación e incluye valores calculados. No se añadieron nutrientes numéricos, ingredientes libres ni tamaños de envase en v1. Esto evita afirmar comparabilidad que no se ha verificado; su presencia archivada queda documentada para un estudio posterior.

# %%
nutrition = pd.read_csv(ROOT/'outputs/nutricion_cobertura_v1.csv', dtype={'product_code':'string'})
display(nutrition.groupby(['per','preparation'],dropna=False).size().to_frame('productos'))
display(nutrition.filter(regex='presente$').sum().to_frame('productos_con_campo'))

# %% [markdown]
# ## Leakage y decisiones de validación futura
# 
# Se excluyen de predictores price_id, hashes, rutas, flags derivados del precio y contenido de proofs que incorpore el objetivo. No se calculan medias de precio ni agregaciones con observaciones futuras. OFF no acredita disponibilidad histórica de sus atributos.
# 
# Un estudio posterior deberá considerar dependencia por producto, ubicación, fecha y proof, así como productos o lugares nuevos. No se supone que un split aleatorio sea válido. Aquí no se divide el dataset ni se entrena un modelo.

# %% [markdown]
# ## Exploración descriptiva conservada
# 
# Se mantiene el ejemplo de Gaufrettes chocolat, código 3760020507916, en EUR. Su función es comprobar que los datos permiten una consulta interpretable, no presentar la descripción como objetivo final. Se comparan importes del mismo código y moneda sin afirmar equivalencia histórica de envase.

# %%
example = d[d.product_code.eq('3760020507916') & d.currency.eq('EUR') & d.qc_price_positive & d.qc_date_valid].copy()
assert len(example) == 32
display(pd.DataFrame([{'observaciones':len(example),'fechas':example.date.nunique(),'ubicaciones':example.location_id.nunique(),'min_EUR':example.price.min(),'max_EUR':example.price.max(),'rango_EUR':example.price.max()-example.price.min()}]))
display(example[['price_id','date','location_id','price']].sort_values(['date','price_id']).head(8))

# %% [markdown]
# El rango observado describe estos registros. No demuestra causas, inflación ni rendimiento predictivo. Las observaciones de un mismo producto no son necesariamente independientes.

# %% [markdown]
# ## Trazabilidad y hashes
# 
# Cada observación enlaza con el hash del core histórico, su ficha OFF y, cuando existe, los metadatos archivados del proof. Las imágenes siguen fuera de esta carpeta por privacidad. Los hashes históricos se verificaron privadamente y aquí solo se identifican.

# %%
lineage = pd.read_csv(ROOT/'data/manifests/linaje_filas_v1.csv', dtype='string')
assert len(lineage) == len(d) and lineage.price_id.is_unique
display(lineage[lineage.price_id.eq('42629')])
display(pd.DataFrame(list(version['outputs_sha256'].items()),columns=['archivo_v1','sha256']))

# %% [markdown]
# ## Reproducción pública y privada
# 
# La reconstrucción siguiente escribe temporales reales CSV/Parquet, verifica equivalencia y compara hashes. No usa Internet ni motores. Empieza en proyecciones públicas: no se confunde con la selección privada desde el core ni con la verificación original de 259 archivos del Notebook histórico.

# %%
result = pipeline.reproduce(ROOT)
assert result['estado'] == 'PASS'
display(result)

# %% [markdown]
# ## Limitaciones y conclusiones
# 
# Se obtuvo una estructura integrada de 485 observaciones y 38 variables, con linaje, derivaciones temporales y roles de variables. Los históricos se preservaron. Las 79 fichas disponibles condicionan la selección; el tamaño, la heterogeneidad monetaria, los faltantes y la falta de versiones históricas impiden prometer una modelización seria sin trabajo adicional.
# 
# Este proyecto construye y documenta el conjunto de datos necesario para una futura tarea de predicción de precios; el entrenamiento y evaluación del modelo quedan fuera del alcance de esta entrega.
# 
# No se usaron modelos, splits, nuevas descargas, OCR ni Spark. El benchmark histórico indicaba que el volumen cabía en memoria; no se repitió. Las bases cuentan con evidencia histórica, no una ejecución nueva en este notebook. La publicación sigue pendiente de autorización.

# %% [markdown]
# ## Referencias
# 
# [Open Prices](https://openfoodfacts.github.io/open-prices/guides/data/), [Open Food Facts API](https://openfoodfacts.github.io/openfoodfacts-server/api/) y [términos OFF](https://world.openfoodfacts.org/terms-of-use). Los manifiestos identifican URLs, hashes y fechas de las fuentes previamente archivadas. Se conserva atribución a Open Prices, Open Food Facts y sus contribuyentes. No se consultaron nuevas fuentes en esta versión.


