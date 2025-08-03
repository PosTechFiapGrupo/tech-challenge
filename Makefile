# Makefile para gerenciar o projeto tech-challenge

.PHONY: help up down logs test migrate migrate-up migrate-down migrate-create build dev clean status shell install print-docker-compose

# Detecta se "docker compose" está disponível, caso contrário usa "docker-compose"
# make up DOCKER_COMPOSE="docker-compose"

DOCKER_COMPOSE := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make up               - Iniciar o aplicativo com docker compose"
	@echo "  make down             - Parar o aplicativo"
	@echo "  make logs             - Ver logs da aplicação"
	@echo "  make test             - Executar testes da aplicação"
	@echo "  make migrate-up       - Aplicar migrations"
	@echo "  make migrate-down     - Reverter última migration"
	@echo "  make migrate-create MSG=<message> - Criar nova migration"
	@echo "  make build            - Construir imagens Docker"
	@echo "  make dev              - Executar app em modo desenvolvimento"
	@echo "  make clean            - Parar e remover containers, volumes e redes"
	@echo "  make status           - Status dos containers"
	@echo "  make shell            - Entrar no container da aplicação"
	@echo "  make install          - Instalar dependências no container"

# Iniciar aplicação
up:
	$(DOCKER_COMPOSE) up -d

# Parar aplicação  
down:
	$(DOCKER_COMPOSE) down

# Ver logs
logs:
	$(DOCKER_COMPOSE) logs -f app

# Executar testes
test:
	$(DOCKER_COMPOSE) exec app python -m pytest app/test/ -v

# Aplicar migrations
migrate-up:
	$(DOCKER_COMPOSE) exec app alembic upgrade head

# Reverter migration
migrate-down:
	$(DOCKER_COMPOSE) exec app alembic downgrade -1

# Criar nova migration
migrate-create:
	$(DOCKER_COMPOSE) exec app alembic revision --autogenerate -m "$(MSG)"

# Construir imagens
build:
	$(DOCKER_COMPOSE) build

# Executar app em modo desenvolvimento
dev:
	$(DOCKER_COMPOSE) up app

# Parar e remover containers, volumes e redes
clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans

# Status dos containers
status:
	$(DOCKER_COMPOSE) ps

# Entrar no container da aplicação
shell:
	$(DOCKER_COMPOSE) exec app /bin/bash

# Instalar dependências
install:
	$(DOCKER_COMPOSE) exec app pip install -r requirements.txt

# Ver qual comando docker-compose está sendo usado
print-docker-compose:
	@echo "Usando comando Docker Compose: $(DOCKER_COMPOSE)"
