import json
import glob
from pathlib import Path
import pytest
from jsonschema import validate
from pyld import jsonld

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "data" / "schemas" / "jsonschema"
EXAMPLE_DIR = ROOT / "data" / "schemas" / "examples"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_jsonld_files_have_context():
    for p in glob.glob(str(EXAMPLE_DIR / "*.jsonld")):
        data = load_json(p)
        assert "@context" in data


def test_examples_validate_against_jsonschema():
    pairs = {
        "WasteContainer": (SCHEMA_DIR / "WasteContainer.schema.json", EXAMPLE_DIR / "WasteContainer.example.jsonld"),
        "WasteContainerIsle": (SCHEMA_DIR / "WasteContainerIsle.schema.json", EXAMPLE_DIR / "WasteContainerIsle.example.jsonld"),
        "WasteContainerModel": (SCHEMA_DIR / "WasteContainerModel.schema.json", EXAMPLE_DIR / "WasteContainerModel.example.jsonld"),
        "WasteObserved": (SCHEMA_DIR / "WasteObserved.schema.json", EXAMPLE_DIR / "WasteObserved.example.jsonld"),
    }
    for name, (schema_p, example_p) in pairs.items():
        schema = load_json(schema_p)
        example = load_json(example_p)
        # jsonschema validate expects normal JSON structure; examples are NGSI-LD shaped
        validate(instance=example, schema=schema)


def test_relationships_use_urn_pattern():
    example = load_json(EXAMPLE_DIR / "WasteObserved.example.jsonld")
    ref = example.get("refContainer")
    assert ref and ref.get("object") and ref.get("object").startswith("urn:ngsi-ld:")


def test_geoproperties_are_valid_geojson():
    cont = load_json(EXAMPLE_DIR / "WasteContainer.example.jsonld")
    loc = cont.get("location")
    assert loc and loc.get("value") and loc["value"]["type"] in ("Point","Polygon")
