# Recursos PostgreSQL históricos

Los SQL conservan el esquema y consultas ya validados para el core de 307.183 filas. Se copiaron sin cambiar el modelo histórico. No representan una nueva carga de v1 ni son necesarios para reproducirlo.

Las consultas requieren la base histórica y sus datos completos, excluidos de esta carpeta. No ejecutar cargas sobre una base ajena ni interpretar estos archivos como un instalador. La evidencia resumida se encuentra en outputs/postgresql_execution.json. El pipeline v1 integra archivos en Python, sin consultas a motores.
