// La base se selecciona al ejecutar: m1721_004 o m1721_public_demo.
// Cada salida está limitada a campos redistribuibles.
const c=db.getCollection('off_product_snapshots');
// M01 ¿Cuántos documentos conservamos? Una respuesta archivada es un documento.
print(JSON.stringify({id:'M01',resultado:c.countDocuments({})}));
// M02 ¿Cuántas respuestas contienen un producto encontrado?
print(JSON.stringify({id:'M02',resultado:c.countDocuments({found:true})}));
// M03 ¿Cuántas no contienen producto? No se inventan fichas para esos códigos.
print(JSON.stringify({id:'M03',resultado:c.countDocuments({found:false})}));
// M04 ¿Qué ficha corresponde al código exacto? El código se conserva como texto.
print(JSON.stringify({id:'M04',resultado:c.find({requested_code:'3560070283484'},{_id:0,requested_code:1,found:1,'response.product.product_name':1}).limit(3).toArray()}));
// M05 ¿Cómo consultamos un campo anidado? El resultado representa fichas, no precios.
print(JSON.stringify({id:'M05',resultado:c.find({'response.product.nova_group':{$exists:true}},{_id:0,requested_code:1,'response.product.nova_group':1}).sort({requested_code:1}).limit(5).toArray()}));
// M06 ¿Qué fichas tienen una lista de categorías no vacía? .0 consulta el primer elemento.
print(JSON.stringify({id:'M06',resultado:c.find({'response.product.categories_tags.0':{$exists:true}},{_id:0,requested_code:1,'response.product.categories_tags':1}).sort({requested_code:1}).limit(2).toArray()}));
// M07 ¿Cómo se distribuyen las fichas encontradas por NOVA? Cada fila es un grupo, no un precio.
print(JSON.stringify({id:'M07',resultado:c.aggregate([{$match:{found:true}},{$group:{_id:'$response.product.nova_group',fichas:{$sum:1}}},{$sort:{_id:1}},{$project:{_id:0,nova_group:'$_id',fichas:1}}]).toArray()}));
// M08 ¿Qué índices existen realmente? Se consulta el catálogo del motor.
print(JSON.stringify({id:'M08',resultado:c.getIndexes()}));
