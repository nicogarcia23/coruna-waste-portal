from pathlib import Path
import re
import json
from datetime import datetime
import numpy as np
import yaml
from jsonschema import validate as js_validate, ValidationError

def make_rng(seed: int):
    return np.random.default_rng(int(seed))

def district_slug(name: str) -> str:
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def container_id(district, type_, n):
    return f"urn:ngsi-ld:WasteContainer:{district}-{type_}-{n:04d}"

def isle_id(district, n):
    return f"urn:ngsi-ld:WasteContainerIsle:{district}-ISLE-{n:02d}"

def timestamp_compact(dt: datetime):
    return dt.strftime('%Y%m%dT%H%M%SZ')

def load_config(path):
    p = Path(path)
    with p.open() as f:
        return yaml.safe_load(f)

def validate_payload(payload, schema_path):
    try:
        with open(schema_path) as f:
            schema = json.load(f)
        js_validate(payload, schema)
        return True, None
    except ValidationError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)
