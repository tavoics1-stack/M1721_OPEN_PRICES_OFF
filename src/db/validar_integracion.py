"""Compara lecturas reales de los motores con las proyecciones canónicas; solo lectura."""
from ejecutar_bd import ROOT,rows,mjson,save
import json,io,sys
import pandas as pd
from pathlib import Path
def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'LOCAL_FULL'
    database='m1721_004' if mode=='LOCAL_FULL' else 'm1721_public_demo'
    public=ROOT/'M1721_OPEN_PRICES_OFF' if mode=='LOCAL_FULL' else ROOT
    dest=ROOT/'outputs/evidencia_bd';dest=dest if mode=='LOCAL_FULL' else dest/'public_demo'
    cols=list(pd.read_csv(public/'data/inputs/core_enriquecible_v1.csv',nrows=0).columns)
    projection={'_id':0,'requested_code':1,'found':1,'source_sha256':1,'acquired_at':1}
    for k in ['code','product_name','brands','categories_tags','nutriscore_grade','nova_group','last_modified_t']:projection['response.product.'+k]=1
    documents=mjson('db.off_product_snapshots.find({found:true},'+json.dumps(projection)+').sort({requested_code:1}).toArray()',database)
    assert len(documents)==79
    safe=[]
    for d in documents:
        p=d['response']['product'];assert str(p['code'])==d['requested_code']
        safe.append({'product_code':d['requested_code'],**{k:p.get(k) for k in ['product_name','brands','nutriscore_grade']},'categories_tags':json.dumps(p['categories_tags'],ensure_ascii=False,sort_keys=True) if p.get('categories_tags') is not None else None,'nova_group':str(float(p['nova_group'])) if p.get('nova_group') is not None else None,'off_source_sha256':d['source_sha256'],'off_acquired_at':d['acquired_at'],'off_last_modified_t':p.get('last_modified_t'),'off_history_status':'NO_VERIFICABLE_HISTORICAMENTE'})
    off=pd.DataFrame(safe).astype('string').fillna('')
    original_off=pd.read_csv(public/'data/inputs/off_proyeccion_v1.csv',dtype='string',keep_default_na=False)
    off=off[original_off.columns].sort_values('product_code').reset_index(drop=True)
    pd.testing.assert_frame_equal(off,original_off.sort_values('product_code').reset_index(drop=True),check_dtype=False)
    codes=','.join("'"+d['requested_code'].replace("'","''")+"'" for d in documents)
    q='SELECT '+','.join(cols)+' FROM m1721_004.stg_open_prices WHERE price_type=\'PRODUCT\' AND product_code IN ('+codes+') ORDER BY price_id'
    core=pd.DataFrame(rows(q,database),columns=cols).astype('string').fillna('')
    for c in core:
        if c.startswith('qc_'):core[c]=core[c].replace({'t':'True','f':'False'})
    original=pd.read_csv(public/'data/inputs/core_enriquecible_v1.csv',dtype='string',keep_default_na=False)
    pd.testing.assert_frame_equal(core,original,check_dtype=False)
    proof=pd.read_csv(public/'data/inputs/proofs_proyeccion_v1.csv',dtype='string',keep_default_na=False)
    assert proof.proof_id.is_unique and off.product_code.is_unique and core.price_id.is_unique
    joined=core.merge(off,on='product_code',how='left',validate='many_to_one').merge(proof,on='proof_id',how='left',validate='many_to_one')
    dates=pd.to_datetime(joined.date,format='%Y-%m-%d')
    joined['year']=dates.dt.year.astype('string');joined['month']=dates.dt.month.astype('string');joined['day_of_week']=dates.dt.dayofweek.astype('string');joined['proof_metadata_available']=joined.proof_metadata_sha256.notna().astype('string')
    final=pd.read_csv(public/'data/processed/precios_productos_predictive_preparation_v1.csv',dtype='string',keep_default_na=False)
    pd.testing.assert_frame_equal(joined[final.columns].astype('string').fillna(''),final,check_dtype=False)
    save(dest/'integracion.json',{'estado':'PASS','modo':mode,'lecturas':'PostgreSQL staging y documentos MongoDB mediante proyección sanitizada','fuente_proof_secundaria':'proyección canónica de metadatos archivados; no se atribuye a MongoDB','filas_antes':len(core),'filas_despues_off':len(core.merge(off,on='product_code',validate='many_to_one')),'filas_despues_proof':len(joined),'price_id_antes':int(core.price_id.nunique()),'price_id_despues':int(joined.price_id.nunique()),'columnas':38,'productos':79,'igualdad_38_columnas_con_csv_canonico':True,'relacion_entre_motores':'lógica product_code = requested_code = response.product.code; sin FK física entre motores','nova':'Representación textual decimal de la proyección v1 conservada al comparar el valor NOVA del motor'})
    example=documents[next(i for i,d in enumerate(documents) if d['requested_code']=='3560070283484')]
    save(dest/'mongodb/esquema_documental.json',{'database':database,'collection':'off_product_snapshots','tipo_documento':'Respuesta completa privada' if mode=='LOCAL_FULL' else 'Proyección redistribuible, no respuesta completa','rutas_permitidas':{k:'campo observado en documentos del motor' for k in projection if k!='_id'},'arrays_verificados':['response.product.categories_tags'],'opcionales':['response.product','response.product.nova_group','response.product.categories_tags'],'ejemplo_sanitizado':example})
    print('Integración entre motores: PASS, 485 x 38, valores canónicos idénticos')
if __name__=='__main__':main()
