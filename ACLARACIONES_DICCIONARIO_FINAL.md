# Aclaraciones del diccionario final

El empaquetado académico conserva íntegros los 42 archivos del repositorio técnico v1, incluidas sus auditorías, Notebook, manifiesto y hashes. Las siguientes precisiones aclaran expresiones agrupadas de la matriz histórica. No cambian datos, código, reglas QC ni metodología.

qc_price_positive comprueba solamente que price no sea nulo y sea mayor que cero. No exige proof. La referencia a proof en la observación agrupada de la matriz histórica corresponde a qc_core_eligible, no a qc_price_positive.

qc_core_eligible combina precio positivo, moneda presente, fecha válida, proof presente e identidad válida. Depende del objetivo y no es una regla de elegibilidad predictiva. Ambos controles se mantienen fuera de los predictores propuestos.

proof_id y proof_type proceden del snapshot Open Prices y están presentes en las 485 filas. La observación general sobre nulo como no consultado corresponde a los metadatos secundarios, no a estos dos campos.

proof_metadata_available está informado en las 485 filas: 75 True y 410 False. Los campos proof_metadata_sha256, proof_metadata_type y proof_prediction_count están presentes en 75 filas y ausentes en 410. False expresa falta de metadatos archivados en esta versión, no inexistencia de una evidencia en el proveedor.

El diccionario final de 38 variables se incluye en docs/Diccionario_Datos_M1721_Final.xlsx. Tiene las mismas definiciones que el PDF y XLSX académicos. La matriz original se conserva como evidencia versionada; estas precisiones deben acompañar su lectura.

SHA256SUMS.txt sigue verificando los archivos originales de v1. SHA256SUMS_EMPAQUETADO.txt y MANIFEST_EMPAQUETADO.csv cubren además las adiciones de documentación de este empaquetado. Los dos datasets finales y el script de reproducción no han cambiado.

La reproducción continúa mediante reproducir.bat desde tres proyecciones redistribuibles. No utiliza las 83 imágenes ni JSON OFF completos, no reproduce los históricos privados y no instala dependencias. No se ha publicado en GitHub; la licencia del código y la publicación requieren autorización humana.
