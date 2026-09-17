CREATE SCHEMA IF NOT EXISTS m1721_004;
SET search_path TO m1721_004;
CREATE TABLE IF NOT EXISTS stg_open_prices (
 price_id bigint PRIMARY KEY,price_type text,product_code text,category_tag text,
 price numeric(10,3),price_per text,currency text,date date,location_id bigint,
 proof_id bigint,proof_type text,proof_file_path text,proof_mimetype text,country text,city text,
 qc_price_positive boolean,qc_currency_present boolean,qc_date_present boolean,
 qc_date_not_future boolean,qc_date_valid boolean,qc_proof_present boolean,
 qc_proof_visual boolean,qc_product_identity boolean,qc_core_eligible boolean,
 source_snapshot text DEFAULT 'e3cf81a0a08d3875a43c22f79ea6afce716e92f9'
);
CREATE TABLE IF NOT EXISTS productos(product_code text PRIMARY KEY,product_name text,brands text,categories_tags jsonb,nutriscore_grade text,nova_group text);
CREATE TABLE IF NOT EXISTS categorias(category_tag text PRIMARY KEY);
CREATE TABLE IF NOT EXISTS ubicaciones(location_id bigint PRIMARY KEY,country text,city text);
CREATE TABLE IF NOT EXISTS proofs(proof_id bigint PRIMARY KEY,file_path text,mimetype text,proof_type text);
CREATE TABLE IF NOT EXISTS precios(
 id bigint PRIMARY KEY, type text NOT NULL,product_code text REFERENCES productos(product_code),
 category_tag text REFERENCES categorias(category_tag),price numeric(10,3),price_per text,currency text,date date,
 location_id bigint REFERENCES ubicaciones(location_id),proof_id bigint REFERENCES proofs(proof_id),
 qc_core_eligible boolean NOT NULL,
 CONSTRAINT subject_check CHECK ((type='PRODUCT' AND product_code IS NOT NULL AND category_tag IS NULL) OR (type='CATEGORY' AND category_tag IS NOT NULL AND product_code IS NULL))
);
CREATE INDEX IF NOT EXISTS prices_subject_currency ON precios(product_code,currency,date);
CREATE INDEX IF NOT EXISTS prices_proof ON precios(proof_id);
CREATE INDEX IF NOT EXISTS prices_location ON precios(location_id);
CREATE OR REPLACE VIEW vw_precios_productos AS
 SELECT p.id AS price_id,p.type,p.product_code,p.category_tag,p.price,p.price_per,p.currency,p.date,p.location_id,
 u.country,u.city,p.proof_id,f.proof_type,r.product_name,r.brands,p.qc_core_eligible
 FROM precios p LEFT JOIN productos r USING(product_code) LEFT JOIN ubicaciones u USING(location_id) LEFT JOIN proofs f USING(proof_id);
