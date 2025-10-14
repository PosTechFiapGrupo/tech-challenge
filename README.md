# Tech Challenge - API de Oficina

Este projeto implementa uma API REST para gerenciamento de ordens de serviço para uma oficina usando arquitetura hexagonal com FastAPI, SQLAlchemy e MySQL.

## 🎯 Objetivo da Solução

Esta fase do Tech Challenge tem como objetivo implementar uma API completa para gerenciamento de ordens de serviço seguindo os princípios de Clean Architecture e DevOps, incluindo:

- **API REST** para operações CRUD de ordens de serviço
- **Arquitetura Hexagonal** para desacoplamento e testabilidade
- **Containerização** com Docker para facilitar deployment
- **Orquestração** com Kubernetes para escalabilidade
- **Infraestrutura como Código** com Terraform
- **CI/CD** automatizado para deploy contínuo

## 🏗️ Arquitetura da Solução

### Componentes da Aplicação

```
┌─────────────────────────────────────────────────────┐
│                    Presentation Layer               │
│  ┌─────────────────┐  ┌─────────────────────────────┐│
│  │   FastAPI       │  │     Swagger/OpenAPI         ││
│  │   Handlers      │  │     Documentation           ││
│  └─────────────────┘  └─────────────────────────────┘│
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│                 Application Layer                   │
│  ┌─────────────────┐  ┌─────────────────────────────┐│
│  │   Use Cases     │  │      Services &             ││
│  │   (Business     │  │      Validators             ││
│  │    Logic)       │  │                             ││
│  └─────────────────┘  └─────────────────────────────┘│
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│                  Domain Layer                       │
│  ┌─────────────────┐  ┌─────────────────────────────┐│
│  │   Entities      │  │     Repository              ││
│  │   & Events      │  │     Interfaces              ││
│  └─────────────────┘  └─────────────────────────────┘│
└─────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────┐
│               Infrastructure Layer                  │
│  ┌─────────────────┐  ┌─────────────────────────────┐│
│  │   SQLAlchemy    │  │      MySQL Database         ││
│  │   Repositories  │  │      Connection             ││
│  └─────────────────┘  └─────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### Infraestrutura Provisionada

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Local (Minikube)           │
│  ┌─────────────────────────────────────────────────┐│
│  │                 Namespace                       ││
│  │  ┌─────────────┐  ┌─────────────┐               ││
│  │  │   API Pod   │  │   API Pod   │  (Replicas)   ││
│  │  └─────────────┘  └─────────────┘               ││
│  │                                                 ││
│  │  ┌─────────────────────────────────────────────┐││
│  │  │         Service (LoadBalancer)              │││
│  │  └─────────────────────────────────────────────┘││
│  │                                                 ││
│  │  ┌─────────────┐  ┌─────────────────────────────┐││
│  │  │   MySQL     │  │        ConfigMaps &         │││
│  │  │   Pod       │  │        Secrets              │││
│  │  └─────────────┘  └─────────────────────────────┘││
│  │                                                 ││
│  │  ┌─────────────────────────────────────────────┐││
│  │  │        Persistent Volumes                   │││
│  │  └─────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### Fluxo de Deploy

```
Developer → Docker Build → Terraform → Kubernetes → Application
     │            │           │            │            │
     │            │           │            │            └─ Health Checks
     │            │           │            └─ Pod Deployment
     │            │           └─ Infrastructure Provisioning
     │            └─ Container Image
     └─ Code Changes
```
## ⚙️ Parâmetros e Segredos da Pipeline CI/CD

A pipeline CI/CD utiliza **GitHub Actions** e depende de algumas variáveis de ambiente e segredos configurados no repositório.

### 🔐 Segredos Obrigatórios (Settings → Secrets → Actions)
| Nome | Exemplo | Descrição |
|------|----------|------------|
| `SECRET_KEY` | `a4f8b9c2d3e4f567890abcdef123456...` | Chave de segurança usada na API |
| `MYSQL_PASSWORD` | `tech_password` | Senha do banco MySQL |
| `MYSQL_ROOT_PASSWORD` | `root_password` | Senha root usada nos testes |
| `GH_TOKEN` *(ou usar `GITHUB_TOKEN`)* | *(automático)* | Token para push da imagem no GHCR |

### 🌍 Variáveis Opcionais (Settings → Variables → Actions)
| Nome | Exemplo | Descrição |
|------|----------|------------|
| `USERNAME_GH` | `Rian292` | Usuário usado no login do GHCR |
| `MYSQL_USER` | `tech_user` | Usuário do banco |
| `MYSQL_DATABASE` | `tech_challenge` | Banco de dados padrão |
| `K8S_NAMESPACE` | `tech-challenge` | Namespace Kubernetes |
| `K8S_CONTEXT` | `docker-desktop` | Contexto kubectl (opcional) |

## 🚀 Tecnologias

- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python com suporte async
- **MySQL 8.0** - Banco de dados relacional
- **Alembic** - Migrations para SQLAlchemy
- **Docker & Docker Compose** - Containerização
- **Kubernetes** - Orquestração de containers
- **Terraform** - Infraestrutura como código

## 📋 Pré-requisitos

- Docker e Docker Compose
- Make (opcional, para usar os comandos do Makefile)
- kubectl (para deploy em Kubernetes)
- Terraform (para provisionamento de infraestrutura)

## 🛠️ Execução Local

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd tech-challenge
```

### 2. Configurar ambiente

```bash
# Renomeie o arquivo "env-example" para ".env"
cp env-example .env
```

### 3. Subir a aplicação

```bash
# Usando Make
make up

# Ou usando Docker Compose diretamente
docker-compose up -d
```

### 4. Aplicar migrations

```bash
make migrate-up
```

### 5. Popular banco de dados (opcional)

```bash
make populate-db
```

### 6. Acessar a aplicação

- **API**: http://localhost:8000
- **Documentação (Swagger)**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## ☸️ Deploy em Kubernetes

### 1. Iniciar Minikube

```bash
# Iniciar cluster local
minikube start

# Verificar status
kubectl cluster-info
```

### 2. Configurar contexto

```bash
# Definir contexto do kubectl
kubectl config use-context docker-desktop
```

### 3. Aplicar configurações manualmente

```bash
# Aplicar todos os manifestos Kubernetes
kubectl apply -f k8s/

# Verificar status dos pods
kubectl get pods -n tech-challenge

# Verificar serviços
kubectl get services -n tech-challenge
```

### 4. Acessar aplicação

```bash
# Obter URL do serviço
minikube service api-service -n tech-challenge --url

# Ou fazer port-forward
kubectl port-forward service/api-service 8000:80 -n tech-challenge
```

## 🏗️ Provisionamento da Infraestrutura com Terraform

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd tech-challenge
```

### 2. Configurar ambiente

```bash
# Renomeie o arquivo "env-example" para ".env"
cp env-example .env
```

### 3. Provisionar infraestrutura (execução completa)

```bash
# Executar todo o processo de uma vez (incluindo init, plan e apply)
make terraform-run
```

### 4. Provisionar infraestrutura (passo a passo) - Opcional

```bash
# Caso prefira executar comando por comando:
make terraform-init
make terraform-plan
make terraform-apply

# Ou manualmente
cd infra/
terraform init
terraform plan
terraform apply
```

### 5. Verificar recursos criados

```bash
# Verificar namespace criado
kubectl get namespaces

# Verificar todos os recursos
kubectl get all -n tech-challenge
```

### 6. Destruir infraestrutura (quando necessário)

```bash
# Limpa completamente os recursos criados (terraform + docker)
make terraform-clean

# Usando Make - apenas limpa recursos do Terraform
make terraform-destroy

# Ou manualmente
terraform destroy
```

## 📚 Documentação da API

### Acessar Collection Completa

A documentação completa da API está disponível através do Swagger UI:

**URL**: `http://localhost:8000/docs` (ambiente local)

**URL**: `http://localhost:30000/docs` (kubernetes local)

### Autenticação

Para testar as APIs que requerem autenticação, utilize o usuário administrador padrão:

```json
{
  "email": "admin@test.com",
  "senha": "senha123"
}
```
