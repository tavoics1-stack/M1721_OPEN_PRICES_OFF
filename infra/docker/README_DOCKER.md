# Bases de datos M1721 con Docker

Docker permite repetir el entorno de PostgreSQL y MongoDB. Los datos ya existen; levantar los contenedores no descarga fuentes ni inicia una carga automáticamente.

Abra Docker Desktop y compruebe que el Engine está en ejecución. Desde la raíz del proyecto, copie `infra/docker/.env.example` como `.env` en la misma carpeta y sustituya `CHANGE_ME` por contraseñas locales distintas. No publique ese archivo. Si los contenedores ya fueron configurados, conserve su `.env`: cambiarlo no modifica las credenciales guardadas en los volúmenes.

```powershell
docker version
docker compose version
docker compose -f infra/docker/docker-compose.yml pull
docker compose -f infra/docker/docker-compose.yml up -d
docker compose -f infra/docker/docker-compose.yml ps
```

El pull solo es necesario si faltan las imágenes oficiales `postgres:17` y `mongo:8`. Después, use `up -d --pull never` para trabajar con las imágenes locales. Los puertos previstos son `127.0.0.1:5433` y `127.0.0.1:27018`; si están ocupados, cambie únicamente los puertos host en `.env`. No detenga aplicaciones ajenas. Los healthchecks deben indicar healthy antes de cargar.

## Elegir el modo de carga

Con Python y pandas ya disponibles, ejecute desde la raíz uno de estos modos:

```powershell
python -B src/db/ejecutar_bd.py LOCAL_FULL
python -B src/db/validar_integracion.py LOCAL_FULL
```

LOCAL_FULL utiliza el core y las 86 respuestas archivadas que existen solo en el proyecto maestro privado. Conserva la base `m1721_004`, el esquema PostgreSQL `m1721_004` y la colección MongoDB `off_product_snapshots`. No necesita ni consulta Internet. Las rutas son relativas al proyecto.

```powershell
python -B src/db/ejecutar_bd.py PUBLIC_DEMO
python -B src/db/validar_integracion.py PUBLIC_DEMO
```

PUBLIC_DEMO se ejecuta desde la raíz del repositorio público extraído y usa las proyecciones de `data/inputs`. Guarda sus datos en otra base, `m1721_public_demo`, para no sustituir la carga completa. En PostgreSQL conserva el esquema `m1721_004`; en MongoDB utiliza la misma colección con documentos explícitamente marcados como proyecciones. No añade respuestas no encontradas ni simula el contenido privado.

La reproducción pública demuestra el esquema y las consultas utilizando las proyecciones redistribuibles; la reconstrucción histórica completa requiere los originales locales excluidos del repositorio público. `proof_file_path` y `proof_mimetype` permanecen nulos en la demostración pública. Los metadatos secundarios de proofs se leen de su proyección canónica, no se atribuyen a la colección OFF.

El cargador ejecuta las 12 consultas SQL y las 8 MongoDB y guarda resultados acotados en `outputs/evidencia_bd`. Para repetir solo las comprobaciones, añada `--solo-verificar` al primer comando. Las consultas de demostración son de lectura; el cargador separado crea tablas, carga y enriquece entidades de forma explícita.

## Detener y recuperar

```powershell
docker compose -f infra/docker/docker-compose.yml stop
docker compose -f infra/docker/docker-compose.yml start
```

Los volúmenes `m1721_postgres_data` y `m1721_mongodb_data` conservan ambas bases. No elimine los volúmenes para detener los motores. Los nombres `m1721-postgres` y `m1721-mongodb` son exclusivos del proyecto; antes de iniciar en otro equipo, compruebe que no correspondan a otra instalación que deba conservarse.

## Versiones y alcance

En esta ejecución los tags oficiales resolvieron a PostgreSQL 17.11 y MongoDB 8.3.9. MongoDB histórico era 8.0.29; se conserva la versión mayor solicitada, los cuatro índices y los mismos 86 documentos. Los identificadores de imagen y RepoDigest están en `outputs/evidencia_bd/docker_image_versions.txt`. Para fijar exactamente esos binarios en una reproducción posterior, use los digest registrados en lugar de asumir que un tag mutable sigue apuntando a la misma imagen.

La red de Compose usa bridge y los puertos se publican solo en localhost. La ejecución documentada utiliza comandos locales y no consulta fuentes externas. No se incluyen credenciales, datos cargados, volúmenes ni imágenes de proofs en el ZIP. `reproducir.bat` sigue reconstruyendo los dos datasets finales sin necesitar Docker; la demostración de bases es una comprobación adicional.
