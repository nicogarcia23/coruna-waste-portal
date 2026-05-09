import yaml
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OPENAPI = ROOT / "backend" / "contracts" / "openapi" / "phase2-data-model.yaml"


def test_openapi_file_is_valid_yaml():
    with open(OPENAPI, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    assert isinstance(doc, dict)


def test_openapi_has_required_tags():
    with open(OPENAPI, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    tags = {t["name"] for t in doc.get("tags", [])}
    assert {"citizen","operator","admin"}.issubset(tags)


def test_openapi_has_bearer_auth_scheme():
    with open(OPENAPI, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    schemes = doc.get("components", {}).get("securitySchemes", {})
    assert "BearerAuth" in schemes
