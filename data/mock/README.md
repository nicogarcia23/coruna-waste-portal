Phase 3 — Mock data generation and ingestion

Este directorio contiene las utilidades para generar datos mock (espaciales y temporales) y reproducirlos a través de Orion-LD/QuantumLeap.

Prerequisitos
- Python 3.11+ (se recomienda usar el virtualenv del proyecto `.venv`)
- Dependencias del proyecto:

```bash
pip install -r data/mock/requirements.txt
```

Variables de entorno
- Configure los endpoints y credenciales en variables de entorno o en `infra/.env`:

```bash
export ORION_LD_URL=http://localhost:1026
export QUANTUMLEAP_URL=http://localhost:8668
export ORION_SERVICE_PATH=/waste
```

Comandos principales

- Generar datos (dev|mvp|city):

```bash
python data/mock/generate.py --seed dev --random-seed 42
```

Salida: `data/mock/output/<seed>/` con:
- `containers.geojson`, `containers.parquet` (o `containers.csv` si falta pyarrow),
- `isles.geojson`, `models.jsonl`,
- `orion_payloads/` (payloads NGSI-LD listos para enviar),
- `metadata.json`.

- Ingestar entidades actuales a Orion-LD (idempotente, con reintentos):

```bash
python data/mock/ingest_orion.py --seed dev
```

Flags útiles: `--dry-run` valida los payloads sin enviarlos, `--resume` reintenta fallos.

- Reproducir histórico (WasteObserved) a través de Orion-LD (dispara subscripciones a QuantumLeap):

```bash
python data/mock/ingest_historical.py --seed dev --random-seed 42
```

Flags útiles: `--dry-run`, `--workers N`, `--random-seed`.

Make targets
- Desde la raíz del repo (Makefile):

```bash
make mock-generate SEED=dev
make mock-ingest-current SEED=dev
make mock-ingest-historical SEED=dev
make mock-validate SEED=dev
```

Notas de diseño
- Los polígonos de distrito se obtienen preferentemente de Overpass API; existe `fallback_districts.geojson` para ejecuciones offline.
- Todos los IDs son deterministas y reproducibles con `--random-seed`.
- El flujo por defecto reenvía las observaciones a Orion-LD para poblar QuantumLeap vía las suscripciones ya definidas.

Problemas comunes
- Instalación de `geopandas`/`pyproj` puede requerir paquetes del sistema (libgdal, etc.). Si hay problemas, instale los requisitos del sistema antes de `pip install`.
- Si no dispone de `pyarrow` el exporter guarda CSV; los tests aceptan ese fallback.

Tests
- Unitarios (rápidos, sin servicios externos):

```bash
python -m pytest -q data/mock/tests/test_mock_generator.py
```

Soporte y próximos pasos
- Si quiere que ejecute el pipeline completo contra su instacia local de Orion/QuantumLeap puedo hacerlo (necesito que ORION_LD_URL y QUANTUMLEAP_URL estén accesibles desde aquí).
