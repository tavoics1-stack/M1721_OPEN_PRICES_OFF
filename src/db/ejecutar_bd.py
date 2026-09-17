"""Carga explícita y comprobaciones Docker. LOCAL_FULL no redistribuye originales.
PUBLIC_DEMO usa solo las tres proyecciones públicas, en otra base.
No modifica datasets, DDL histórico ni volúmenes existentes ajenos a M1721.
"""
from pathlib import Path
import argparse,csv,io,json,subprocess,shutil,time,hashlib,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
DOCKER=shutil.which('docker')
if not DOCKER:raise RuntimeError('Docker no está en PATH; abra una terminal con Docker Desktop disponible')
def command(args,content=None):
    p=subprocess.run([DOCKER]+args,input=content,capture_output=True,encoding='utf-8',errors='strict',cwd=ROOT)
    if p.returncode:raise RuntimeError('Docker falló: '+p.stderr[:1400])
    return p.stdout
def save(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def pg(query,db,content=None,csvmode=True):
    args=['exec','-i','m1721-postgres','psql','-X','-q','-v','ON_ERROR_STOP=1','-U','m1721','-d',db]
    if csvmode:args+=['--csv']
    return command(args+['-c',query],content)
def rows(query,db):return list(csv.DictReader(io.StringIO(pg(query,db))))
def mongo(script,db):
    shell='exec mongosh --quiet --username "$MONGO_INITDB_ROOT_USERNAME" --password "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin "$1" --file /dev/stdin'
    return command(['exec','-i','m1721-mongodb','sh','-c',shell,'m1721',db],script)
def mjson(script,db):return json.loads(mongo('print(JSON.stringify('+script+'));',db).strip())
def healthy():
    for _ in range(40):
        states=[json.loads(command(['inspect','--format','{{json .State}}',n])) for n in ['m1721-postgres','m1721-mongodb']]
        if all(s['Running'] and s.get('Health',{}).get('Status')=='healthy' for s in states):return
        time.sleep(2)
    raise RuntimeError('Healthcheck no completado')
def load(mode,db):
    import pandas as pd
    if mode=='LOCAL_FULL':
        core=pd.read_csv(ROOT/'data/curated/open_prices_core_curated.csv',dtype='string',keep_default_na=False)
        docs=[json.loads(s) for s in (ROOT/'data/processed/off_product_snapshots.jsonl').read_text(encoding='utf-8').splitlines()]
        for d in docs:
            p=ROOT/'data/source_archive/open_food_facts'/(d['requested_code']+'.json')
            assert hashlib.sha256(p.read_bytes()).hexdigest()==d['source_sha256']
            assert json.loads(p.read_bytes())==d['response']
        assert len(core)==307183 and len(docs)==86
    else:
        core=pd.read_csv(ROOT/'data/inputs/core_enriquecible_v1.csv',dtype='string',keep_default_na=False)
        off=pd.read_csv(ROOT/'data/inputs/off_proyeccion_v1.csv',dtype='string',keep_default_na=False)
        core['proof_file_path']='';core['proof_mimetype']=''
        docs=[]
        for r in off.to_dict('records'):
            p={k:r[k] or None for k in ['product_name','brands','nutriscore_grade','nova_group']}
            p.update(code=r['product_code'],categories_tags=json.loads(r['categories_tags']) if r['categories_tags'] else None,last_modified_t=int(r['off_last_modified_t']) if r['off_last_modified_t'] else None)
            # Esta estructura es una proyección explícita, nunca una respuesta API completa.
            docs.append({'requested_code':r['product_code'],'source_sha256':r['off_source_sha256'],'acquired_at':r['off_acquired_at'],'found':True,'response':{'product':p},'representation':'PUBLIC_PROJECTION_NOT_RAW_API'})
        assert len(core)==485 and len(docs)==79
    for key,cols in [('location_id',['country','city']),('proof_id',['proof_file_path','proof_mimetype','proof_type'])]:
        dim=core.loc[core[key].ne(''),[key]+cols].drop_duplicates()
        assert not dim[key].duplicated().any(),key
    pg((ROOT/'sql/05_etapa004_schema.sql').read_text(encoding='utf-8'),db,csvmode=False)
    n=int(rows('SELECT count(*) AS n FROM m1721_004.stg_open_prices',db)[0]['n'])
    if n==0:
        pg('COPY m1721_004.stg_open_prices ('+','.join(core.columns)+') FROM STDIN WITH (FORMAT CSV,HEADER TRUE)',db,core.to_csv(index=False,lineterminator='\n'),False)
    else:assert n==len(core),'Base contiene otra carga; no sobrescribir'
    pg((ROOT/'sql/06_etapa004_load.sql').read_text(encoding='utf-8'),db,csvmode=False)
    # Mismos cuatro índices de la ejecución histórica, incluido _id.
    script="const c=db.off_product_snapshots;c.createIndex({requested_code:1,source_sha256:1},{unique:true});c.createIndex({'response.product.brands':1});c.createIndex({'response.product.categories_tags':1});const docs="+json.dumps(docs,ensure_ascii=True)+";for(const d of docs){const prior=c.findOne({requested_code:d.requested_code,source_sha256:d.source_sha256});if(prior && JSON.stringify(prior.response)!==JSON.stringify(d.response))throw Error('Documento previo distinto');c.updateOne({requested_code:d.requested_code,source_sha256:d.source_sha256},{$setOnInsert:d},{upsert:true});}print(JSON.stringify({documents:c.countDocuments({})}));"
    result=json.loads(mongo(script,db));assert result['documents']==len(docs)
    # Mantiene el enriquecimiento de productos del runner histórico.
    def lit(x):return 'NULL' if x is None else "'"+str(x).replace("'","''")+"'"
    statements=[]
    for d in docs:
        p=d['response'].get('product') or {}
        if d['found']:
            vals=[lit(p.get(k)) for k in ['product_name','brands']]+[lit(json.dumps(p.get('categories_tags'),ensure_ascii=False))+'::jsonb',lit(p.get('nutriscore_grade')),lit(p.get('nova_group'))]
            statements.append('UPDATE m1721_004.productos SET '+','.join(k+'='+v for k,v in zip(['product_name','brands','categories_tags','nutriscore_grade','nova_group'],vals))+' WHERE product_code='+lit(d['requested_code'])+';')
    pg('BEGIN;'+''.join(statements)+'COMMIT;',db,csvmode=False)
    return core,docs
def verify(mode,db,dest):
    qtext=(ROOT/'sql/consultas_demostrativas_m1721.sql').read_text(encoding='utf-8')
    queries=[q.strip() for q in '\n'.join(l for l in qtext.splitlines() if not l.startswith('--')).split(';') if q.strip()]
    assert len(queries)==12 and all(q.startswith('SELECT') for q in queries)
    for i,q in enumerate(queries,1):save(dest/f'postgresql/queries/{i:02}.csv',pg(q,db))
    counts={r['tabla']:int(r['filas']) for r in rows(queries[3],db)}
    expected=dict(zip(['stg_open_prices','productos','categorias','precios','ubicaciones','proofs'],[307183,135700,593,307183,6608,113917] if mode=='LOCAL_FULL' else [485,79,0,485,148,None]))
    for t,n in counts.items():assert expected[t] is None or n==expected[t],(t,n,expected[t])
    schema="""SELECT t.table_name AS tabla,t.column_name AS columna,t.data_type AS tipo,t.is_nullable AS nullable,
    EXISTS(SELECT 1 FROM pg_constraint c WHERE c.conrelid=cl.oid AND c.contype='p' AND a.attnum=ANY(c.conkey)) AS primary_key,
    EXISTS(SELECT 1 FROM pg_constraint c WHERE c.conrelid=cl.oid AND c.contype='f' AND a.attnum=ANY(c.conkey)) AS foreign_key,
    COALESCE((SELECT string_agg(pg_get_constraintdef(c.oid),' | ') FROM pg_constraint c WHERE c.conrelid=cl.oid AND c.contype='f' AND a.attnum=ANY(c.conkey)),'') AS referencia,
    EXISTS(SELECT 1 FROM pg_constraint c WHERE c.conrelid=cl.oid AND c.contype IN ('u','p') AND a.attnum=ANY(c.conkey)) AS unique,
    COALESCE((SELECT string_agg(c.conname||': '||pg_get_constraintdef(c.oid),' | ') FROM pg_constraint c WHERE c.conrelid=cl.oid AND a.attnum=ANY(c.conkey)),'') AS constraint
    FROM information_schema.columns t JOIN pg_namespace ns ON ns.nspname=t.table_schema JOIN pg_class cl ON cl.relnamespace=ns.oid AND cl.relname=t.table_name JOIN pg_attribute a ON a.attrelid=cl.oid AND a.attname=t.column_name
    WHERE t.table_schema='m1721_004' AND cl.relkind='r' ORDER BY t.table_name,t.ordinal_position"""
    save(dest/'postgresql/esquema_real.csv',pg(schema,db))
    for name,kind in [('pk','p'),('fk','f'),('checks','c'),('unique','u')]:
        save(dest/f'postgresql/{name}.csv',pg("SELECT conrelid::regclass::text AS tabla,conname,pg_get_constraintdef(oid) AS definicion,convalidated FROM pg_constraint WHERE connamespace='m1721_004'::regnamespace AND contype='"+kind+"' ORDER BY conname",db))
    save(dest/'postgresql/indexes.csv',pg("SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='m1721_004' ORDER BY tablename,indexname",db))
    cards=[]
    for table,key in [('productos','product_code'),('categorias','category_tag'),('ubicaciones','location_id'),('proofs','proof_id')]:
        empirical=rows(f"SELECT (SELECT count(*) FROM m1721_004.precios WHERE {key} IS NULL) AS precios_sin_clave,min(n) AS minimo_observado,max(n) AS maximo_observado,count(*) FILTER(WHERE n=0) AS entidades_sin_precio FROM (SELECT d.{key},count(p.id) AS n FROM m1721_004.{table} d LEFT JOIN m1721_004.precios p USING({key}) GROUP BY d.{key}) x",db)[0]
        cards.append({'relacion':table+' - precios','lado_a':'0..N precios por entidad','lado_b':'0..1 entidad por precio','ddl':'FK formal; PK destino; FK nullable y no UNIQUE','optionalidad':'producto obligatorio en PRODUCT; categoría obligatoria en CATEGORY' if table in ['productos','categorias'] else 'opcional por precio','evidencia_empirica':json.dumps(empirical),'interpretacion':'El DDL permite entidades sin precios; el rango observado no reemplaza la cardinalidad del esquema'})
    s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(cards[0]));w.writeheader();w.writerows(cards);save(dest/'postgresql/cardinalidades.csv',s.getvalue())
    ms=mongo((ROOT/'nosql/consultas_mongodb_m1721.js').read_text(encoding='utf-8'),db)
    result=[json.loads(l) for l in ms.splitlines() if l.startswith('{')];assert len(result)==8
    for r in result:save(dest/f'mongodb/queries/{r["id"]}.json',r)
    assert [r['resultado'] for r in result[:3]]==([86,79,7] if mode=='LOCAL_FULL' else [79,79,0])
    assert len(result[7]['resultado'])==4
    save(dest/'mongodb/indexes.json',result[7]['resultado'])
    summary={'modo':mode,'database':db,'schema':'m1721_004','collection':'off_product_snapshots','conteos_pg':counts,'mongodb':{'documentos':result[0]['resultado'],'encontrados':result[1]['resultado'],'no_encontrados':result[2]['resultado'],'indices':4},'version_postgres':rows('SELECT version()',db)[0]['version'],'version_mongodb':mjson('db.version()',db),'sql_ejecutadas':12,'mongo_ejecutadas':8,'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'PASS'}
    save(dest/'resumen.json',summary);return summary
def main():
    ap=argparse.ArgumentParser();ap.add_argument('modo',choices=['LOCAL_FULL','PUBLIC_DEMO']);ap.add_argument('--solo-verificar',action='store_true');args=ap.parse_args()
    db='m1721_004' if args.modo=='LOCAL_FULL' else 'm1721_public_demo'
    dest=ROOT/'outputs/evidencia_bd';dest=dest if args.modo=='LOCAL_FULL' else dest/'public_demo'
    healthy()
    if not rows("SELECT datname FROM pg_database WHERE datname='"+db+"'",'postgres'):pg('CREATE DATABASE '+db,'postgres',csvmode=False)
    if not args.solo_verificar:load(args.modo,db)
    summary=verify(args.modo,db,dest)
    if args.modo=='LOCAL_FULL':
        save(dest/'docker_compose_ps.txt',command(['compose','-f','infra/docker/docker-compose.yml','ps']))
        save(dest/'docker_image_versions.txt','\n'.join(command(['image','inspect',n,'--format','{{json .RepoTags}} {{.Id}} {{json .RepoDigests}}']) for n in ['postgres:17','mongo:8']))
        save(dest/'docker_versions.txt',command(['version','--format','{{json .}}'])+'\n'+command(['compose','version']))
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
