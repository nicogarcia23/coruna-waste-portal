COMPOSE = docker compose --env-file infra/.env -f infra/docker-compose.yml
PYTHON ?= $(shell if [ -x "$(CURDIR)/.venv/bin/python" ]; then echo "$(CURDIR)/.venv/bin/python"; elif command -v python3 >/dev/null 2>&1; then command -v python3; else command -v python; fi)

.PHONY: up up-all all down logs ps reset backend-local frontend-local seed-mock-data

up:
	$(COMPOSE) up -d

up-all:
	$(COMPOSE) up -d --wait mqtt-broker mongodb orion-ld timescaledb quantumleap redis vroom backend-api frontend grafana
	$(COMPOSE) up -d orion-subscriber
	$(MAKE) seed-mock-data

seed-mock-data: mock-generate mock-ingest-current

all: up-all

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f --tail=200

ps:
	$(COMPOSE) ps

reset:
	@read -r -p "This will stop containers and remove volumes. Continue? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(COMPOSE) down -v; \
	else \
		echo "Aborted."; \
	fi

backend-local:
	cd backend && $(PYTHON) -m pip install -r requirements.txt && $(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

frontend-local:
	cd frontend && npm install && npm start

.PHONY: mock-generate mock-ingest-current mock-ingest-historical mock-validate

SEED ?= dev

mock-generate:
	cd data/mock && $(PYTHON) generate.py --seed $(SEED)

mock-ingest-current:
	cd data/mock && $(PYTHON) ingest_orion.py --seed $(SEED)

mock-ingest-historical:
	cd data/mock && $(PYTHON) ingest_historical.py --seed $(SEED)

mock-validate:
	cd data/mock && $(PYTHON) -m pytest tests/test_mock_generator.py -q

.PHONY: db-init-policies

db-init-policies:
	cd infra/db && bash init.sh
