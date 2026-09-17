# Ejecución de bases de datos M1721

Comprobamos PostgreSQL 17.11 y MongoDB 8.3.9 mediante Docker Engine 29.7.2 y Compose 5.5.1. La etiqueta mongo:8 resolvió a 8.3.9; el histórico utilizaba 8.0.29. No modificamos metodología ni datasets canónicos.

LOCAL_FULL conserva m1721_004, seis tablas PostgreSQL, seis PK, cuatro FK y subject_check. La vista tiene 307183 filas e identificadores únicos. MongoDB conserva 86 respuestas, 79 encontradas y siete no encontradas, con cuatro índices. Ejecutamos 12 SELECT y ocho consultas MongoDB; sus salidas sanitizadas están en postgresql/queries y mongodb/queries. Las versiones abreviadas del informe también se ejecutaron y están en queries_informe.

PUBLIC_DEMO se ejecutó desde la carpeta pública separada con sus proyecciones: 485 precios, 79 productos, 148 ubicaciones, 404 referencias de proof y 79 fichas OFF. Las 38 columnas reconstruidas en memoria coinciden con el CSV canónico, tanto en LOCAL_FULL como en PUBLIC_DEMO. Las fichas se relacionan por código exacto; no hay FK entre motores.

persistencia.json registra iguales conteos antes y después de stop/start en ambas bases. estado_final_contenedores.json documenta que, al finalizar aquella verificación, m1721-postgres y m1721-mongodb quedaron detenidos y los volúmenes m1721_postgres_data y m1721_mongodb_data se conservaron; no es una consulta de su estado actual. Para reactivar: docker compose -f infra/docker/docker-compose.yml start.

La evidencia automática se complementa con las seis capturas PG-1, PG-2, PG-3, MG-1, MG-2 y MG-3, ya realizadas e incorporadas en M1721_ENTREGA_FINAL_REORIENTADA/05_EVIDENCIA_VISUAL_BD/Evidencia_Visual_PostgreSQL_MongoDB_M1721.docx (ruta desde la raíz del proyecto maestro; el DOCX se entrega fuera de este ZIP). Las seis imágenes se verificaron visualmente en la auditoría documental del 2026-09-12. La guía actualizada está en docs/GUIA_CAPTURAS_PGADMIN_COMPASS.md de este ZIP y en la carpeta de evidencia de la entrega académica. La observación histórica sobre paginación nativa del informe DOCX por ausencia de LibreOffice no equivale a falta de capturas y no se da por resuelta en esta auditoría; el PDF fue revisado por separado.
