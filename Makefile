COMPOSE = docker compose --env-file infra/.env -f infra/docker-compose.yml

.PHONY: up up-all down logs ps reset

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