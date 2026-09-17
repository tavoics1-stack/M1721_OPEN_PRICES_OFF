-- Q01 ¿Qué tablas organizan los datos? Cada fila identifica una tabla.
SELECT table_name FROM information_schema.tables WHERE table_schema='m1721_004' AND table_type='BASE TABLE' ORDER BY table_name;
-- Q02 ¿Qué claves primarias existen? Son constraints del motor.
SELECT conrelid::regclass::text AS tabla,conname,pg_get_constraintdef(oid) AS definicion FROM pg_constraint WHERE connamespace='m1721_004'::regnamespace AND contype='p' ORDER BY tabla;
-- Q03 ¿Qué relaciones tienen FK formal? No incluye la unión lógica con MongoDB.
SELECT conrelid::regclass::text AS tabla,conname,pg_get_constraintdef(oid) AS definicion FROM pg_constraint WHERE connamespace='m1721_004'::regnamespace AND contype='f' ORDER BY conname;
-- Q04 ¿Cuántas filas hay en cada entidad? No sumar entidades de granularidad diferente.
SELECT 'stg_open_prices' AS tabla,count(*) AS filas FROM m1721_004.stg_open_prices UNION ALL SELECT 'productos',count(*) FROM m1721_004.productos UNION ALL SELECT 'categorias',count(*) FROM m1721_004.categorias UNION ALL SELECT 'precios',count(*) FROM m1721_004.precios UNION ALL SELECT 'ubicaciones',count(*) FROM m1721_004.ubicaciones UNION ALL SELECT 'proofs',count(*) FROM m1721_004.proofs;
-- Q05 ¿Cómo es una observación real? id se presenta como price_id.
SELECT id AS price_id,type AS price_type,product_code,category_tag,price,currency,date FROM m1721_004.precios ORDER BY id LIMIT 10;
-- Q06 ¿Cómo se incorpora la ficha de un producto? Cada fila sigue siendo un precio.
SELECT p.id AS price_id,p.product_code,r.product_name,p.price,p.currency FROM m1721_004.precios p JOIN m1721_004.productos r USING(product_code) WHERE r.product_name IS NOT NULL ORDER BY p.id LIMIT 10;
-- Q07 ¿Dónde se registró cada precio? La PK de ubicaciones evita multiplicar filas.
SELECT p.id AS price_id,p.location_id,u.country,u.city,p.price,p.currency FROM m1721_004.precios p JOIN m1721_004.ubicaciones u USING(location_id) ORDER BY p.id LIMIT 10;
-- Q08 ¿Qué ocurre si falta proof_id? LEFT JOIN conserva la observación.
SELECT p.id AS price_id,p.proof_id,f.proof_type,p.price,p.currency FROM m1721_004.precios p LEFT JOIN m1721_004.proofs f USING(proof_id) ORDER BY p.proof_id NULLS FIRST,p.id LIMIT 10;
-- Q09 ¿Puede un producto tener varios precios? GROUP BY cambia la unidad a producto.
SELECT product_code,count(*) AS observaciones FROM m1721_004.precios WHERE type='PRODUCT' GROUP BY product_code HAVING count(*)>1 ORDER BY observaciones DESC,product_code LIMIT 10;
-- Q10 ¿Cómo se distinguen PRODUCT y CATEGORY? Los identificadores no son simultáneamente obligatorios.
SELECT type,count(*) AS filas,count(product_code) AS con_producto,count(category_tag) AS con_categoria FROM m1721_004.precios GROUP BY type ORDER BY type;
-- Q11 ¿Se conserva la identidad de los precios? Ambos conteos deben coincidir.
SELECT count(*) AS filas,count(DISTINCT id) AS price_id_unicos FROM m1721_004.precios;
-- Q12 ¿La vista conserva una fila por precio? El total acompaña una muestra limitada.
SELECT price_id,type,product_code,price,currency,country,city,proof_id,product_name,count(*) OVER() AS total_vista FROM m1721_004.vw_precios_productos ORDER BY price_id LIMIT 10;
