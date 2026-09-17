-- Las restricciones se crean en schema.sql; esta consulta comprueba su validación.
SELECT conname,contype,convalidated FROM pg_constraint WHERE connamespace='m1721_004'::regnamespace ORDER BY conname;
