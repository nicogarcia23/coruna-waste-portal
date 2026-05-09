import json
from pathlib import Path
import geopandas as gpd
import pandas as pd

def write_geojson(gdf, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(str(p), driver='GeoJSON')

def write_parquet(df, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Use pandas to write parquet if available
    df.to_parquet(str(p))

def write_jsonl(records, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

def write_orion_payloads(entities, output_dir):
    p = Path(output_dir)
    p.mkdir(parents=True, exist_ok=True)
    for ent in entities:
        fname = p / (ent.get('id').replace(':','_') + '.jsonld')
        with fname.open('w', encoding='utf-8') as f:
            json.dump(ent, f, ensure_ascii=False)
