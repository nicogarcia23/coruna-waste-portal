Phase 3 mock data generation and ingestion

Quick start:

1. Install dependencies (in project venv):

```bash
pip install -r data/mock/requirements.txt
```

2. Generate dev seed:

```bash
python data/mock/generate.py --seed dev --random-seed 42
```

Outputs are written to `data/mock/output/<seed>/`.

Use `ingest_orion.py` and `ingest_historical.py` to push data to Orion-LD.
