# Makefile para gerenciar o projeto tech-challenge

.PHONY: help up down logs test migrate migrate-up migrate-down migrate-create build

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make up           - Iniciar o aplicativo com docker-compose"
	@echo "  make down         - Parar o aplicativo"
	@echo "  make logs         - Ver logs da aplicação"
	@echo "  make test         - Executar testes da aplicação"
	@echo "  make migrate-up   - Aplicar migrations"
	@echo "  make migrate-down - Reverter última migration"
	@echo "  make migrate-create MSG=<message> - Criar nova migration"
	@echo "  make build        - Construir imagens Docker"

# Iniciar aplicação
up:
	docker-compose up -d

# Parar aplicação  
down:
	docker-compose down

# Ver logs
logs:
	docker-compose logs -f app

# Executar testes
test:
	docker-compose exec app python -m pytest app/test/ -v

# Aplicar migrations
migrate-up:
	docker-compose exec app alembic upgrade head

# Reverter migration
migrate-down:
	docker-compose exec app alembic downgrade -1

# Criar nova migration
migrate-create:
	docker-compose exec app alembic revision --autogenerate -m "$(MSG)"

# Construir imagens
build:
	docker-compose build

# Executar app em modo desenvolvimento
dev:
	docker-compose up app

# Parar e remover containers, volumes e redes
clean:
	docker-compose down -v --remove-orphans

# Status dos containers
status:
	docker-compose ps

# Entrar no container da aplicação
shell:
	docker-compose exec app /bin/bash

# Instalar dependências
install:
	docker-compose exec app pip install -r requirements.txt
