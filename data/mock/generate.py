#!/usr/bin/env python3
import argparse
from pathlib import Path
from datetime import datetime
import json
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon

from .utils import make_rng, district_slug, container_id, isle_id, load_config, timestamp_compact
from .districts import fetch_district_polygons
from .exporters import write_geojson, write_parquet, write_jsonl, write_orion_payloads

DISTRICT_NAMES = [
    "Cidade Vella/Centro","Ensanche-Juan Flórez","Monte Alto","Riazor-Orzán",
    "Os Mallos-Sagrada Familia","Cuatro Caminos","Os Castros","Eirís",
    "Os Rosales","Matogrande/Palavea","A Grela"
]

def distribute_counts(total, weights):
    # weights is dict name->weight
    names = list(weights.keys())
    w = np.array([weights[n] for n in names], dtype=float)
    w = w / w.sum()
    raw = w * total
    counts = np.floor(raw).astype(int)
    # distribute remainder
    rem = int(total - counts.sum())
    if rem > 0:
        idx = np.argsort(- (raw - counts))
        for i in range(rem):
            counts[idx[i % len(counts)]] += 1
    return dict(zip(names, counts))

def make_models(cfg):
    models = cfg['models']
    return models

def sample_points_in_polygon(poly: Polygon, n, rng):
    minx, miny, maxx, maxy = poly.bounds
    points = []
    attempts = 0
    while len(points) < n and attempts < n * 20:
        x = rng.uniform(minx, maxx)
        y = rng.uniform(miny, maxy)
        p = Point(x, y)
        if poly.contains(p):
            points.append(p)
        attempts += 1
    # if not enough points, fall back to centroid jitter
    while len(points) < n:
        c = poly.representative_point()
        jitter = Point(c.x + rng.uniform(-1e-4,1e-4), c.y + rng.uniform(-1e-4,1e-4))
        points.append(jitter)
    return points

def generate(seed_name, random_seed, output_dir):
    cfg = load_config(Path(__file__).parent / 'config.yaml')
    seed_cfg = cfg['seeds'][seed_name]
    total = seed_cfg['total_containers']
    rng = make_rng(int(random_seed))

    # districts
    out_dir = Path(output_dir) / seed_name
    out_dir.mkdir(parents=True, exist_ok=True)
    districts_gdf = fetch_district_polygons(DISTRICT_NAMES, out_dir / 'districts.geojson')
    # compute counts per district
    counts = distribute_counts(total, cfg['district_weights'])

    models = make_models(cfg)

    containers = []
    isles = []
    model_records = []
    orion_entities = []
    idx = 1
    # create isles and containers
    for dname in DISTRICT_NAMES:
        slug = district_slug(dname)
        n = counts.get(dname, 0)
        # create one isle per district for small seeds, otherwise calculate
        num_isles = seed_cfg.get('isles_per_district', 1)
        if 'target_containers_per_isle' in seed_cfg:
            num_isles = max(1, int(np.ceil(n / seed_cfg['target_containers_per_isle'])))
        isle_centroids = []
        # get polygon
        row = districts_gdf[districts_gdf['name'] == dname]
        if row.empty:
            poly = Polygon([(-8.39,43.37),(-8.385,43.37),(-8.385,43.365),(-8.39,43.365)])
        else:
            poly = row.iloc[0].geometry
        # generate isles
        for i in range(num_isles):
            cent = poly.representative_point()
            isle = {
                'id': isle_id(slug, i+1),
                'district': dname,
                'name': f'{dname} ISLE {i+1}',
                'geometry': cent
            }
            isles.append(isle)
            isle_centroids.append(cent)

        # sample container points
        pts = sample_points_in_polygon(poly, n, rng)
        for k,p in enumerate(pts, start=1):
            # choose type by global mix
            types = list(cfg['waste_type_mix'].keys())
            probs = np.array([cfg['waste_type_mix'][t] for t in types])
            probs = probs / probs.sum()
            t = rng.choice(types, p=probs)
            # choose model weighted among those supporting the type
            model_candidates = [m for m in models if t in m['types']]
            weights = np.array([m['weight'] for m in model_candidates], dtype=float)
            if weights.sum() == 0:
                weights = np.ones(len(model_candidates))
            weights = weights / weights.sum()
            chosen = rng.choice(model_candidates, p=weights)
            cid = container_id(slug, t, idx)
            # assign isle by nearest centroid
            nearest_idx = 0
            if isle_centroids:
                dists = [p.distance(c) for c in isle_centroids]
                nearest_idx = int(np.argmin(dists))
            cont = {
                'id': cid,
                'district': dname,
                'type': t,
                'model': chosen['id'],
                'isle': isle_id(slug, nearest_idx+1),
                'geometry': p,
                'fillLevel': float(rng.uniform(0.1,0.9)),
            }
            containers.append(cont)
            # create simple NGSI-LD payload
            ent = {
                'id': cid,
                'type': 'WasteContainer',
                'location': {
                    'type': 'GeoProperty',
                    'value': {'type':'Point','coordinates':[p.x, p.y]}
                },
                'model': {'type':'Property','value': chosen['id']},
                'isle': {'type':'Relationship','object': isle_id(slug, nearest_idx+1)}
            }
            orion_entities.append(ent)
            idx += 1

    # write outputs
    # containers.geojson
    gdf = gpd.GeoDataFrame([{ 'id': c['id'], 'district': c['district'], 'type': c['type'], 'model': c['model'], 'isle': c['isle'], 'fillLevel': c['fillLevel'], 'geometry': c['geometry'] } for c in containers], crs='EPSG:4326')
    write_geojson(gdf, out_dir / 'containers.geojson')
    write_parquet(pd.DataFrame([{'id':c['id'],'district':c['district'],'type':c['type'],'model':c['model'],'isle':c['isle'],'fillLevel':c['fillLevel'],'lon':c['geometry'].x,'lat':c['geometry'].y} for c in containers]), out_dir / 'containers.parquet')

    # isles
    isles_gdf = gpd.GeoDataFrame([{ 'id': i['id'], 'district': i['district'], 'name': i['name'], 'geometry': i['geometry'] } for i in isles], crs='EPSG:4326')
    write_geojson(isles_gdf, out_dir / 'isles.geojson')

    # models
    for m in models:
        model_records.append({'id': m['id'], 'capacity': m['capacity'], 'types': m['types']})
    write_jsonl(model_records, out_dir / 'models.jsonl')

    # orion payloads
    write_orion_payloads(orion_entities, out_dir / 'orion_payloads')

    metadata = {
        'seed': seed_name,
        'random_seed': int(random_seed),
        'total_containers': len(containers),
        'generated_at': datetime.utcnow().isoformat() + 'Z'
    }
    with open(out_dir / 'metadata.json','w') as f:
        json.dump(metadata, f)

    print('Generated', len(containers), 'containers at', out_dir)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', default='dev')
    p.add_argument('--random-seed', default=42)
    p.add_argument('--output-dir', default=str(Path(__file__).parent / 'output'))
    args = p.parse_args()
    generate(args.seed, args.random_seed, args.output_dir)

if __name__ == '__main__':
    main()
