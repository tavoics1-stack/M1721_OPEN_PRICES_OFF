"""Reconstrucción offline desde proyecciones redistribuibles, no desde el archivo privado."""
from pathlib import Path
import argparse, csv, hashlib, json, os, socket, sys, tempfile
from decimal import Decimal
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NAME = 'precios_productos_predictive_preparation_v1'
INPUTS = ['core_enriquecible_v1.csv', 'off_proyeccion_v1.csv', 'proofs_proyeccion_v1.csv']

def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def block_network():
    def denied(*args, **kwargs):
        raise RuntimeError('La reproducción no permite acceso de red')
    socket.create_connection = denied
    socket.socket.connect = denied
    socket.socket.connect_ex = denied

def build(root=ROOT):
    root = Path(root).resolve()
    src = root / 'data/inputs'
    core, off, proof = [pd.read_csv(src / n, dtype='string', keep_default_na=False) for n in INPUTS]
    for d in (core, off, proof):
        d.replace('', pd.NA, inplace=True)
    assert core.price_id.is_unique and core.price_id.notna().all()
    assert off.product_code.is_unique and off.product_code.notna().all()
    assert proof.proof_id.is_unique and proof.proof_id.notna().all()
    assert core.price_type.eq('PRODUCT').all()
    assert set(core.product_code) == set(off.product_code)
    n = len(core)
    d = core.merge(off, on='product_code', how='left', validate='many_to_one')
    assert len(d) == n and d.off_source_sha256.notna().all()
    d = d.merge(proof, on='proof_id', how='left', validate='many_to_one')
    assert len(d) == n and d.price_id.is_unique
    dates = pd.to_datetime(d.date, format='%Y-%m-%d', errors='coerce')
    d['year'] = dates.dt.year.astype('Int64')
    d['month'] = dates.dt.month.astype('Int64')
    d['day_of_week'] = dates.dt.dayofweek.astype('Int64')
    d['proof_metadata_available'] = d.proof_metadata_sha256.notna().astype('boolean')
    for c in ['price_id', 'location_id', 'proof_id', 'proof_prediction_count', 'off_last_modified_t']:
        d[c] = pd.to_numeric(d[c], errors='raise').astype('Int64')
    for c in d:
        if c.startswith('qc_'):
            assert d[c].dropna().isin(['True', 'False']).all()
            d[c] = d[c].map({'True': True, 'False': False}).astype('boolean')
    d['price'] = d.price.map(lambda x: None if pd.isna(x) else Decimal(x))
    d = d.sort_values('price_id').reset_index(drop=True)
    return d

def write_pair(d, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    paths = [folder / (NAME + '.' + ext) for ext in ['csv', 'parquet']]
    d.to_csv(paths[0], index=False, lineterminator='\n')
    d.to_parquet(paths[1], index=False, compression='snappy')
    a = pd.read_csv(paths[0], dtype='string', keep_default_na=False)
    b = pd.read_parquet(paths[1]).astype('string').fillna('')
    pd.testing.assert_frame_equal(a, b, check_dtype=False)
    return {p.name: sha(p) for p in paths}

def reproduce(root=ROOT):
    block_network()
    root = Path(root).resolve()
    expected = json.loads((root / 'data/manifests/version_v1.json').read_text(encoding='utf-8'))
    for rel, h in expected['inputs_sha256'].items():
        p = (root / rel).resolve()
        assert p.is_relative_to(root) and sha(p) == h, rel
    d = build(root)
    # Reconstrucción real en directorio local temporal; nunca sobrescribe finales.
    with tempfile.TemporaryDirectory(prefix='reproduccion_', dir=root / 'outputs') as temp:
        hashes = write_pair(d, temp)
    assert hashes == expected['outputs_sha256']
    for name, h in hashes.items():
        assert sha(root / 'data/processed' / name) == h
    assert list(d.shape) == expected['shape']
    return {'estado': 'PASS', 'modo': 'OFFLINE_DESDE_PROYECCIONES', 'shape': list(d.shape),
            'price_id_unicos': int(d.price_id.nunique()), 'hashes': hashes,
            'alcance': 'Reconstruye v1 desde proyecciones incluidas; no verifica originales privados excluidos.'}

if __name__ == '__main__':
    # La ejecución por consola restringe los accesos operativos a esta copia.
    # Las bibliotecas del intérprete son entorno, no fuentes de datos del proyecto.
    allowed = [ROOT.resolve(), Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()]
    allowed += [Path(x).resolve() for x in os.environ.get('PYTHONPATH', '').split(os.pathsep) if x]
    def guard(event, args):
        if event.startswith('socket.'):
            raise RuntimeError('Red bloqueada durante reproducción')
        if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(args[0])).resolve()
            if not any(p.is_relative_to(folder) for folder in allowed):
                raise RuntimeError('Acceso fuera de la copia y bibliotecas del intérprete')
    sys.addaudithook(guard)
    print(json.dumps(reproduce(), ensure_ascii=False, indent=2))
