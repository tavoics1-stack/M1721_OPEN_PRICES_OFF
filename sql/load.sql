SET search_path TO m1721_004;
INSERT INTO productos(product_code) SELECT DISTINCT product_code FROM stg_open_prices WHERE product_code IS NOT NULL ON CONFLICT DO NOTHING;
INSERT INTO categorias SELECT DISTINCT category_tag FROM stg_open_prices WHERE category_tag IS NOT NULL ON CONFLICT DO NOTHING;
-- El runner valida previamente que no haya atributos contradictorios por clave.
INSERT INTO ubicaciones SELECT DISTINCT location_id,country,city FROM stg_open_prices WHERE location_id IS NOT NULL ON CONFLICT DO NOTHING;
INSERT INTO proofs SELECT DISTINCT proof_id,proof_file_path,proof_mimetype,proof_type FROM stg_open_prices WHERE proof_id IS NOT NULL ON CONFLICT DO NOTHING;
INSERT INTO precios SELECT price_id,price_type,product_code,category_tag,price,price_per,currency,date,location_id,proof_id,qc_core_eligible FROM stg_open_prices ON CONFLICT DO NOTHING;
