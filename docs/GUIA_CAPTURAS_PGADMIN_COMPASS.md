# Capturas de PostgreSQL y MongoDB

Grupo 2

Las consultas y cargas ya se comprobaron con Docker. Las seis capturas manuales PG-1, PG-2, PG-3, MG-1, MG-2 y MG-3 ya están realizadas e incorporadas en Evidencia_Visual_PostgreSQL_MongoDB_M1721.docx, en 05_EVIDENCIA_VISUAL_BD de la entrega académica M1721_ENTREGA_FINAL_REORIENTADA, fuera de este ZIP. Esta guía conserva los pasos utilizados como referencia; no exige repetir las capturas, cargar datos ni descargar fuentes. Los nombres de algunos botones pueden variar con la versión instalada.

## Preparación

En una terminal situada en la raíz del proyecto privado M1721, ejecutar:

```bat
docker compose -f infra/docker/docker-compose.yml start
docker compose -f infra/docker/docker-compose.yml ps
```

Esperar a que ambos servicios indiquen healthy. Los volúmenes existentes contienen las bases completas y la demostración pública. Si la base esperada no aparece, detener la captura y revisar el estado; no crear otra base ni inventar resultados. En una copia pública nueva, seguir primero infra/docker/README_DOCKER.md para PUBLIC_DEMO; las capturas PG de esta guía utilizan la base completa ya preparada en el maestro privado.

Consultar las credenciales únicamente en el archivo local infra/docker/.env. No capturar ni compartir ese archivo. PostgreSQL usa POSTGRES_USER y POSTGRES_PASSWORD; MongoDB utiliza MONGO_ROOT_USER y MONGO_ROOT_PASSWORD. El usuario configurado es m1721. No pegar contraseñas en consultas ni incluirlas en nombres de conexión.

## PG-1 Conexión

Aplicación: pgAdmin 4. En el árbol izquierdo, clic derecho en Servers, Register, Server. En General escribir M1721 local. En Connection introducir Host name/address 127.0.0.1, Port 5433, Maintenance database m1721_004, Username m1721 y la contraseña local de PostgreSQL. Guardar. Expandir el servidor y Databases; seleccionar m1721_004. Abrir Tools, Query Tool y ejecutar con el botón Execute:

```sql
SELECT version() AS version_postgresql,
       current_database() AS base,
       5433 AS puerto_localhost,
       inet_server_port() AS puerto_interno;
```

Esperado: PostgreSQL 17.11, base m1721_004, puerto del equipo 5433 y puerto interno 5432. Estos dos puertos son distintos por el mapeo de Docker. Ajustar el ancho de las columnas para leerlos. Deben verse el servidor conectado, la base, el SQL y Data Output. No mostrar la pestaña de contraseña, el archivo .env ni otros servidores personales.

Texto bajo la figura: “Conectamos pgAdmin a la base m1721_004 mediante localhost:5433. PostgreSQL informa la versión 17.11; el puerto 5432 corresponde al servicio dentro del contenedor.”

## PG-2 Modelo relacional

Aplicación: pgAdmin 4, servidor M1721 local, base m1721_004. Expandir Schemas, m1721_004, Tables. En el menú contextual del esquema usar ERD For Schema, si está disponible. Como alternativa, abrir Tools, ERD Tool y arrastrar las tablas desde el explorador al lienzo. Conservar únicamente stg_open_prices, productos, categorias, ubicaciones, proofs y precios; no añadir tablas de otras bases. Usar Auto align/Auto layout y ajustar el zoom hasta que sean legibles los seis nombres y las relaciones. No guardar cambios DDL ni ejecutar SQL generado por el editor. Esta operación solo visualiza el esquema.

Las PK son stg_open_prices.price_id, productos.product_code, categorias.category_tag, ubicaciones.location_id, proofs.proof_id y precios.id. Las cuatro FK salen de precios: product_code, category_tag, location_id y proof_id, hacia las PK homónimas de sus entidades. Cada entidad puede tener varios precios: relación 1:N, con mínimo permitido 0 precios. Desde un precio, cada referencia nullable admite 0..1 entidad. subject_check exige producto en PRODUCT o categoría en CATEGORY. Staging no tiene una FK hacia precios; su correspondencia es de carga. La vista presenta precios.id como price_id.

Comprobación de solo lectura en Query Tool, si se necesita contrastar las líneas:

```sql
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE connamespace='m1721_004'::regnamespace AND contype='f'
ORDER BY conname;
```

Esperado: cuatro restricciones. El ERD de referencia está en docs/diagramas/ERD_PostgreSQL_M1721.svg del ZIP. La figura PG-2 del DOCX muestra el ERD en pgAdmin; el SVG es evidencia derivada del catálogo, no una captura de pgAdmin. No dibujar una FK hacia MongoDB ni unir staging artificialmente. No mostrar credenciales ni otros proyectos.

Texto bajo la figura: “Organizamos cada observación en precios, cuya PK id se presenta como price_id. Cuatro claves foráneas la relacionan con productos, categorías, ubicaciones y proofs. El vínculo con MongoDB es lógico y no forma parte de estas restricciones.”

## PG-3 Consulta con JOIN

Aplicación: pgAdmin 4, Query Tool de m1721_004. Pegar y ejecutar Q07, idéntica a sql/consultas_demostrativas_m1721.sql:

```sql
SELECT p.id AS price_id,p.location_id,u.country,u.city,p.price,p.currency FROM m1721_004.precios p JOIN m1721_004.ubicaciones u USING(location_id) ORDER BY p.id LIMIT 10;
```

Esperado: 10 filas. Las primeras tres tienen price_id 1, 2 y 3, location_id 1, France, Grenoble; precios 27.700, 27.700 y 26.380 EUR. La representación de decimales puede variar. Ampliar Data Output y mantener visibles código, cabeceras y resultados. Antes y después del JOIN, una fila representa un precio; la PK de ubicaciones impide multiplicaciones. Este INNER JOIN excluye la observación sin ubicación; la vista completa usa LEFT JOIN. No mostrar pestañas privadas ni datos ajenos.

Texto bajo la figura: “Relacionamos precios y ubicaciones mediante location_id para identificar dónde se registró cada observación. Cada fila del resultado conserva un price_id; la unión incorpora país y ciudad sin multiplicar precios.”

## MG-1 Base y colección

Aplicación: MongoDB Compass. Abrir Add New Connection y usar esta URI sin contraseña:

```text
mongodb://127.0.0.1:27018/?authSource=admin
```

En las opciones de Authentication seleccionar Username/Password, usuario m1721, contraseña local de MongoDB y Authentication Database admin. Conectar. Cerrar el diálogo de credenciales. Seleccionar la base m1721_public_demo y la colección off_product_snapshots. Abrir Documents, borrar filtros y pulsar Find/Refresh. El filtro vacío es:

```json
{}
```

Esperado: 79 documentos. La captura debe incluir nombre de servidor, base, colección y contador. La colección completa privada m1721_004 no se usa para capturas MongoDB. Si el contador está estimado o desactualizado, refrescar y comprobar en Aggregations con [{"$count":"documentos"}], que debe devolver 79. No mostrar URI con contraseña, .env ni bases ajenas.

Texto bajo la figura: “La demostración pública conserva 79 fichas OFF proyectadas en m1721_public_demo.off_product_snapshots. Cada documento representa una ficha de producto; no equivale a una observación de precio ni a una respuesta privada completa.”

## MG-2 Documento público proyectado

Aplicación: MongoDB Compass, misma base y colección pública. En Documents, Filter pegar:

```json
{"requested_code":"3560070283484"}
```

Abrir Options y en Project pegar:

```json
{"_id":0,"requested_code":1,"found":1,"response.product.code":1,"response.product.product_name":1,"response.product.categories_tags":1}
```

Pulsar Find. Seleccionar vista JSON o expandir response, product y categories_tags. Esperado: una ficha encontrada de Épinards, código 3560070283484 y su lista de categorías. Esta proyección sigue la selección segura de M04, con code y categories_tags del documento público para enseñar su estructura. Deben verse el filtro, el código, el objeto anidado y el array. No expandir ni mostrar respuestas de la base privada, contributor data, contactos, imágenes o contenido de predicciones.

Texto bajo la figura: “Consultamos una ficha por su código exacto. El objeto response.product contiene atributos y un array de categorías; esta estructura admite campos opcionales sin convertir cada documento en una fila rígida.”

## MG-3 Consulta de un array

Aplicación: MongoDB Compass, Documents de m1721_public_demo.off_product_snapshots. Usar Filter:

```json
{"response.product.categories_tags.0":{"$exists":true}}
```

En Options, Project:

```json
{"_id":0,"requested_code":1,"response.product.categories_tags":1}
```

En Sort pegar {"requested_code":1} y en Limit escribir 2; pulsar Find. Es equivalente a M06 de nosql/consultas_mongodb_m1721.js. Esperado: dos fichas, requested_code 00204682 y 0021130306022, con listas no vacías. Mantener visibles filtro, proyección, orden, límite y ambas salidas; el contador global del filtro puede ser mayor que dos, porque Limit restringe la salida. No mostrar campos privados.

Texto bajo la figura: “Consultamos la primera posición del array categories_tags para seleccionar listas no vacías. La salida muestra dos fichas ordenadas por código; cada documento puede relacionarse posteriormente con varios precios.”

## Cierre y estado de evidencia

Las seis imágenes están incorporadas como figuras PG-1, PG-2, PG-3, MG-1, MG-2 y MG-3 en Evidencia_Visual_PostgreSQL_MongoDB_M1721.docx. Estos identificadores nombran las figuras; no implican que existan seis archivos PNG separados en este ZIP. La auditoría documental no modifica las imágenes ni constituye una nueva autorización de publicación.

La evidencia técnica ya se reprodujo mediante Docker y scripts: 12 consultas SQL, 8 consultas MongoDB, integración de 485 filas y 38 columnas y persistencia tras reinicio. Las seis capturas de interfaces complementan esa evidencia y se verificaron visualmente en la auditoría documental del 2026-09-12. Para detener los contenedores tras una sesión, desde la raíz del proyecto:

```bat
docker compose -f infra/docker/docker-compose.yml stop
```

Este comando conserva las bases y los volúmenes. No utilizar down -v.
