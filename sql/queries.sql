-- Una sentencia por consulta; se ejecutan realmente mediante el runner.
SELECT product_code,count(*) AS n FROM m1721_004.precios WHERE type='PRODUCT' GROUP BY product_code ORDER BY n DESC,product_code LIMIT 20;
SELECT currency,count(*) AS n FROM m1721_004.precios GROUP BY currency ORDER BY n DESC;
SELECT min(date),max(date) FROM m1721_004.precios;
SELECT product_code,count(*) AS n FROM m1721_004.precios WHERE type='PRODUCT' GROUP BY product_code HAVING count(*)>1 ORDER BY n DESC,product_code LIMIT 20;
SELECT location_id,count(*) AS n FROM m1721_004.precios GROUP BY location_id ORDER BY n DESC LIMIT 20;
SELECT count(*) AS con_proof FROM m1721_004.precios WHERE proof_id IS NOT NULL;
SELECT proof_id,count(*) AS n FROM m1721_004.precios WHERE proof_id IS NOT NULL GROUP BY proof_id HAVING count(*)>1 ORDER BY n DESC LIMIT 20;
SELECT count(*) AS productos_sin_nombre_OFF FROM m1721_004.productos WHERE product_name IS NULL;
SELECT 'duplicate_of NO_DISPONIBLE_EN_PARQUET - NO_USADO' AS estado;
SELECT type,product_code,category_tag,currency,price_per,count(*) AS n,min(price),max(price),max(price)-min(price) AS variacion_observada FROM m1721_004.precios WHERE qc_core_eligible GROUP BY type,product_code,category_tag,currency,price_per HAVING count(*)>1 ORDER BY n DESC LIMIT 20;
SELECT * FROM m1721_004.vw_precios_productos ORDER BY price_id LIMIT 20;
SELECT count(*) AS filas,count(DISTINCT price_id) AS ids FROM m1721_004.vw_precios_productos;
