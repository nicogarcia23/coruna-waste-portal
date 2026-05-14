#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import os
import httpx
import sys

# ensure local package imports work when executed as a script
HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

try:
    from .utils import make_rng, timestamp_compact
except ImportError:
    from utils import make_rng, timestamp_compact

CORE_CONTEXT = ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]

def generate_series(container, days, interval_minutes, rng, cfg):
    periods = int((days * 24 * 60) / interval_minutes)
    now = datetime.utcnow()
    times = [now - timedelta(minutes=interval_minutes * (periods - i)) for i in range(periods)]
    fill = []
    val = rng.uniform(0.1,0.4)
    for t in times:
        # simple increase
        val = val + rng.uniform(0.0, 0.01)
        if rng.uniform() < cfg['fill_behavior']['overflow_probability']:
            v = rng.uniform(1.0, 1.5)
        else:
            v = val
        v = max(0.0, min(1.5, v))
        fill.append((t, v))
    return fill

def replay(seed, random_seed, dry_run=False):
    out = Path(__file__).parent / 'output' / seed
    df = pd.read_parquet(out / 'containers.parquet')
    rng = make_rng(int(random_seed))
    ORION_LD_URL = os.getenv('ORION_LD_URL', 'http://localhost:1026')
    client = httpx.Client(timeout=30)
    created = 0
    failed = 0
    for _, row in df.iterrows():
        series = generate_series(row, days=7, interval_minutes=60, rng=rng, cfg={ 'fill_behavior': { 'overflow_probability': 0.0 } })
        for t,v in series[:10]:
            ent = {
                'id': f"urn:ngsi-ld:WasteObserved:{row['id']}-{timestamp_compact(t)}",
                'type': 'WasteObserved',
                'dateObserved': {'type':'Property','value': t.isoformat() + 'Z'},
                'fillLevel': {'type':'Property','value': float(v * 100)},
                '@context': CORE_CONTEXT,
            }
            if not dry_run:
                r = client.post(ORION_LD_URL + '/ngsi-ld/v1/entities', json=ent, headers={'Content-Type':'application/ld+json'})
                if r.status_code in (201, 204):
                    created += 1
                elif r.status_code == 409:
                    created += 1
                else:
                    failed += 1
    if not dry_run:
        client.close()
        print(f'Historical observations sent: {created}, failed: {failed}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', default='dev')
    p.add_argument('--random-seed', default=42)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    replay(args.seed, args.random_seed, args.dry_run)

if __name__ == '__main__':
    main()
