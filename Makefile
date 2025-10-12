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
	@echo "  make build        - Construir imagens Docker"
	@echo "  make install      - Instalar dependências"
	@echo "  make install-dev  - Instalar dependências de desenvolvimento"
	@echo "  make format       - Formatar código com Black"
	@echo "  make format-check - Verificar formatação sem alterar arquivos"
	@echo "  make lint         - Executar linting com flake8"
	@echo "  make check-all    - Executar formatação, lint e testes"
	@echo "  make populate-db  - Popular banco de dados com dados fictícios"

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
	$(DOCKER_COMPOSE) exec app python -m pytest app/test/ -v --disable-warnings

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

build-up:
	$(DOCKER_COMPOSE) up -d --build

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

# Instalar dependências de desenvolvimento
install-dev:
	$(DOCKER_COMPOSE) exec app pip install -r requirements.txt
	$(DOCKER_COMPOSE) exec app pip install black flake8 pytest pytest-asyncio

# Formatar código com Black
format:
	$(DOCKER_COMPOSE) exec app black app/

# Verificar formatação sem alterar arquivos
format-check:
	$(DOCKER_COMPOSE) exec app black app/ --check --diff

# Executar linting com flake8
lint:
	$(DOCKER_COMPOSE)exec app flake8 app/

# Executar formatação, lint e testes
check-all: format lint test
	@echo "✅ Formatação, linting e testes concluídos!"

# Popular banco de dados com dados fictícios
populate-db:
	$(DOCKER_COMPOSE) exec app python populate_db.py

# Ver qual comando docker-compose está sendo usado
print-docker-compose:
	@echo "Usando comando Docker Compose: $(DOCKER_COMPOSE)"
APP_NAME := tech-challenge-app
IMAGE_TAG := latest
IMAGE_NAME := $(APP_NAME):$(IMAGE_TAG)
INFRA_DIR := infra

# ================================================
# DOCKER
# ================================================

docker-build-image:
	docker build -t $(IMAGE_NAME) .

docker-clean:
	docker system prune -af --volumes

# ================================================
# TERRAFORM
# ===========

terraform-init:
	cd $(INFRA_DIR) && terraform init

terraform-plan:
	cd $(INFRA_DIR) && terraform plan

terraform-apply:
	cd $(INFRA_DIR) && terraform apply -auto-approve

terraform-destroy:
	cd $(INFRA_DIR) && terraform destroy -auto-approve

terraform-output:
	cd $(INFRA_DIR) && terraform output

terraform-validate:
	cd $(INFRA_DIR) && terraform validate

# ================================================
# KUBERNETES
# ================================================

kube-get:
	kubectl get pods,svc,jobs,hpa

kube-logs:
	kubectl logs deploy/$(APP_NAME) --tail=100

kube-describe:
	kubectl describe deploy/$(APP_NAME)

# ================================================
# WORKFLOW COMPLETO
# ================================================

# Executa todo o fluxo: build + terraform init/apply + exibe status do cluster
terraform-run: docker-build-image terraform-init terraform-apply kube-get

# Destrói toda a infra e limpa imagens
terraform-clean: terraform-destroy docker-clean
