COMPOSE = docker compose --env-file infra/.env -f infra/docker-compose.yml

.PHONY: up up-all down logs ps reset backend-local frontend-local

up:
	$(COMPOSE) up -d

up-all:
	$(COMPOSE) --profile app up -d

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

PYTHON ?= python
SEED ?= dev

mock-generate:
	cd data/mock && $(PYTHON) generate.py --seed $(SEED)

mock-ingest-current:
	cd data/mock && $(PYTHON) ingest_orion.py --seed $(SEED)

mock-ingest-historical:
	cd data/mock && $(PYTHON) ingest_historical.py --seed $(SEED)

mock-validate:
	cd data/mock && $(PYTHON) -m pytest tests/test_mock_generator.py -q
