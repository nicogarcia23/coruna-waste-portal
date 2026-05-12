#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
from pathlib import Path
import httpx
from tqdm.asyncio import tqdm

# ensure local package imports work when executed as a script
HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from utils import load_config

CORE_CONTEXT = ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]


def ensure_context(entity: dict) -> dict:
    """Attach a local NGSI-LD context if the payload does not define one."""
    if "@context" in entity:
        return entity

    payload = dict(entity)
    payload["@context"] = CORE_CONTEXT
    return payload

async def post_entity(client, url, ent, semaphore):
    async with semaphore:
        try:
            payload = ensure_context(ent)
            r = await client.post(url + '/ngsi-ld/v1/entities', json=payload, headers={'Content-Type':'application/ld+json'})
            if r.status_code in (201, 204):
                return True, None
            if r.status_code == 409:
                # conflict: update attributes
                eid = payload['id']
                attrs = {k:v for k,v in payload.items() if k not in ('id','type','@context')}
                pr = await client.patch(url + f'/ngsi-ld/v1/entities/{eid}/attrs', json=attrs, headers={'Content-Type':'application/ld+json'})
                return pr.status_code in (204,200), pr.text
            return False, r.text
        except Exception as e:
            return False, str(e)

async def run(seed, dry_run=False):
    cfg = load_config(Path(__file__).parent / 'config.yaml')
    out = Path(__file__).parent / 'output' / seed / 'orion_payloads'
    # read env ORION_LD_URL
    import os
    ORION_LD_URL = os.getenv('ORION_LD_URL', 'http://localhost:1026')
    files = list(out.glob('*.jsonld'))
    if dry_run:
        print('Dry run: would process', len(files), 'entities')
        return
    client = httpx.AsyncClient(timeout=30)
    sem = asyncio.Semaphore(cfg['ingestion']['concurrency'])
    tasks = [post_entity(client, ORION_LD_URL, json.loads(p.read_text(encoding='utf-8')), sem) for p in files]
    results = []
    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        ok, msg = await coro
        results.append((ok,msg))
    await client.aclose()
    successes = sum(1 for r in results if r[0])
    failures = len(results) - successes
    print(f'Sent {successes}, failed {failures}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', default='dev')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    asyncio.run(run(args.seed, args.dry_run))

if __name__ == '__main__':
    main()
