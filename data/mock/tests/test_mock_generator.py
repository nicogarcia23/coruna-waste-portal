import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / 'output' / 'dev'

def run_generate():
    cmd = [sys.executable, str(ROOT / 'generate.py'), '--seed', 'dev', '--random-seed', '42']
    subprocess.check_call(cmd)

def test_determinism(tmp_path):
    # run twice and compare metadata + containers.parquet sizes
    run_generate()
    m1 = json.loads((OUT / 'metadata.json').read_text())
    # run again
    run_generate()
    m2 = json.loads((OUT / 'metadata.json').read_text())
    assert m1['random_seed'] == m2['random_seed']
    assert m1['total_containers'] == m2['total_containers']

def test_container_counts_match_config():
    import yaml
    cfg = yaml.safe_load((ROOT / 'config.yaml').read_text())
    expected = cfg['seeds']['dev']['total_containers']
    import pandas as pd
    try:
        df = pd.read_parquet(OUT / 'containers.parquet')
    except Exception:
        # fallback to CSV if parquet engine is not available
        df = pd.read_csv(OUT / 'containers.csv')
    assert len(df) == expected

def test_fallback_geojson_exists():
    f = ROOT / 'fallback_districts.geojson'
    assert f.exists()
