# Tech Challenge - API de Produtos

Este projeto implementa uma API REST para gerenciamento de produtos usando arquitetura hexagonal (ports and adapters) com FastAPI, SQLAlchemy e MySQL.

## 🏗️ Arquitetura

O projeto segue a arquitetura hexagonal com as seguintes camadas:

- **Domain**: Entidades, repositórios abstratos, use cases e eventos de domínio
- **Application**: Serviços de aplicação e validadores
- **Infrastructure**: Implementação de repositórios, handlers HTTP, models do banco de dados e configurações

## 🚀 Tecnologias

- **Python 3.12**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python com suporte async
- **MySQL 8.0** - Banco de dados relacional
- **Alembic** - Migrations para SQLAlchemy
- **Docker & Docker Compose** - Containerização
- **Dependency Injector** - Injeção de dependências

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Make (opcional, para usar os comandos do Makefile)

## 🛠️ Como executar

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd tech-challenge
```

### 2. Subir a aplicação

```bash
# Usando Make
make up

# Ou usando Docker Compose diretamente
docker-compose up -d
```

### 3. Aplicar migrations

```bash
# Usando Make
make migrate-up

# Ou usando Docker Compose diretamente
docker-compose exec app alembic upgrade head
```

### 4. Popular banco de dados (opcional)

Para popular o banco com dados fictícios para testes:

```bash
# Usando Make
make populate-db
```

### 5. Acessar a aplicação

- API: http://localhost:8000
- Documentação (Swagger): http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## 📝 Comandos disponíveis (Makefile)

```bash
make help           # Exibir ajuda com todos os comandos
make up             # Iniciar o aplicativo
make down           # Parar o aplicativo
make logs           # Ver logs da aplicação
make test           # Executar testes da aplicação
make migrate-up     # Aplicar migrations
make migrate-down   # Reverter última migration
make migrate-create MSG="mensagem" # Criar nova migration
make build          # Construir imagens Docker
make dev            # Executar em modo desenvolvimento
make clean          # Parar e remover containers, volumes e redes
make status         # Status dos containers
make shell          # Entrar no container da aplicação
```

## 🏗️ Estrutura do Projeto

O projeto segue os princípios da **Clean Architecture**, organizando o código em camadas bem definidas:

```
tech-challenge/
├── app/
│   ├── application/               # Camada de Aplicação
│   │   ├── services/             # Serviços de aplicação
│   │   │   ├── cliente.py        # Serviço de clientes
│   │   │   ├── servico.py        # Serviço de serviços
│   │   │   ├── ordem_servico.py  # Serviço de ordens de serviço
│   │   │   ├── product.py        # Serviço de produtos
│   │   │   ├── user.py           # Serviço de usuários
│   │   │   └── vehicle.py        # Serviço de veículos
│   │   └── validators/           # Validadores de negócio
│   │       ├── cliente.py        # Validador de clientes
│   │       ├── servico.py        # Validador de serviços
│   │       ├── product_validator.py
│   │       ├── user_validator.py
│   │       └── vehicle_validator.py
│   │
│   ├── domain/                   # Camada de Domínio
│   │   ├── entities/            # Entidades de domínio
│   │   │   ├── cliente.py       # Entidade Cliente
│   │   │   ├── servico.py       # Entidade Serviço
│   │   │   ├── ordem_servico.py # Entidade Ordem de Serviço
│   │   │   ├── status_ordem_servico.py # Enum de Status
│   │   │   ├── product.py       # Entidade Produto
│   │   │   ├── user.py          # Entidade Usuário
│   │   │   └── vehicle.py       # Entidade Veículo
│   │   ├── events/              # Eventos de domínio
│   │   │   ├── cliente.py       # Eventos de cliente
│   │   │   ├── servico.py       # Eventos de serviço
│   │   │   └── product.py       # Eventos de produto
│   │   ├── exceptions.py        # Exceções de domínio
│   │   ├── repositories/        # Interfaces de repositórios
│   │   │   ├── cliente.py       # Interface repositório cliente
│   │   │   ├── servico.py       # Interface repositório serviço
│   │   │   ├── ordem_servico.py # Interface repositório OS
│   │   │   ├── product.py       # Interface repositório produto
│   │   │   ├── user.py          # Interface repositório usuário
│   │   │   └── vehicle.py       # Interface repositório veículo
│   │   └── use_cases/           # Casos de uso
│   │       ├── cliente.py       # Casos de uso de cliente
│   │       ├── servico.py       # Casos de uso de serviço
│   │       ├── ordem_servico.py # Casos de uso de OS
│   │       ├── product.py       # Casos de uso de produto
│   │       ├── user.py          # Casos de uso de usuário
│   │       └── vehicle.py       # Casos de uso de veículo
│   │
│   ├── infrastructure/          # Camada de Infraestrutura
│   │   ├── database.py          # Configuração do banco de dados
│   │   ├── fast_api.py          # Configuração do FastAPI
│   │   ├── container.py         # Container de injeção de dependência
│   │   ├── auth_dependencies.py # Dependências de autenticação
│   │   ├── handlers/            # Controllers/Handlers HTTP
│   │   │   ├── clientes.py      # Endpoints de clientes
│   │   │   ├── servicos.py      # Endpoints de serviços
│   │   │   ├── ordem_servico.py # Endpoints de ordens de serviço
│   │   │   ├── products.py      # Endpoints de produtos
│   │   │   ├── users.py         # Endpoints de usuários
│   │   │   └── vehicles.py      # Endpoints de veículos
│   │   ├── models/              # Modelos SQLAlchemy
│   │   │   ├── cliente.py       # Modelo de cliente
│   │   │   ├── servico.py       # Modelo de serviço
│   │   │   ├── ordem_servico.py # Modelo de ordem de serviço
│   │   │   ├── product.py       # Modelo de produto
│   │   │   ├── user.py          # Modelo de usuário
│   │   │   └── vehicle.py       # Modelo de veículo
│   │   ├── repositories/        # Implementações de repositórios
│   │   │   ├── cliente_impl.py  # Implementação repositório cliente
│   │   │   ├── servico_impl.py  # Implementação repositório serviço
│   │   │   ├── ordem_servico_impl.py # Implementação repositório OS
│   │   │   ├── product_impl.py  # Implementação repositório produto
│   │   │   ├── user_impl.py     # Implementação repositório usuário
│   │   │   └── vehicle_impl.py  # Implementação repositório veículo
│   │   ├── schemas/             # Schemas Pydantic
│   │   │   ├── cliente.py       # Schemas de cliente
│   │   │   ├── servico.py       # Schemas de serviço
│   │   │   ├── ordem_servico.py # Schemas de ordem de serviço
│   │   │   ├── product_schema.py# Schemas de produto
│   │   │   ├── user_schema.py   # Schemas de usuário
│   │   │   └── vehicle_schema.py# Schemas de veículo
│   │   └── events/              # Implementações de eventos
│   │       ├── cliente_impl.py  # Implementação eventos cliente
│   │       ├── servico_impl.py  # Implementação eventos serviço
│   │       └── product_impl.py  # Implementação eventos produto
│   │
│   ├── test/                    # Testes
│   │   ├── fastapi/            # Testes de API
│   │   │   ├── test_cliente_api.py
│   │   │   ├── test_servico_api.py
│   │   │   ├── test_ordem_servico_api.py
│   │   │   ├── test_product_api.py
│   │   │   ├── test_user_api.py
│   │   │   └── test_vehicle_api.py
│   │   ├── services/           # Testes de serviços
│   │   │   ├── test_cliente.py
│   │   │   ├── test_servico.py
│   │   │   ├── test_product.py
│   │   │   └── test_user.py
│   │   └── entities/           # Testes de entidades
│   │       ├── test_cliente.py
│   │       ├── test_servico.py
│   │       └── test_product.py
│   │
│   └── main.py                 # Ponto de entrada da aplicação
│
├── migrations/                 # Migrações do banco de dados
│   ├── versions/              # Versões das migrações
│   ├── alembic.ini           # Configuração do Alembic
│   ├── env.py                # Ambiente de migração
│   └── script.py.mako        # Template de migração
│
├── docker-compose.yml          # Configuração do Docker Compose
├── Dockerfile                  # Imagem Docker da aplicação
├── Makefile                   # Comandos de automação
├── requirements.txt           # Dependências Python
├── pyproject.toml            # Configuração do projeto
├── .flake8                   # Configuração do linting
└── README.md                 # Documentação do projeto
```

### 🎯 Princípios Arquiteturais

- **Clean Architecture**: Separação clara entre camadas de domínio, aplicação e infraestrutura
- **Dependency Inversion**: Uso de interfaces e injeção de dependência
- **Single Responsibility**: Cada classe tem uma responsabilidade específica
- **SOLID Principles**: Aplicação dos princípios SOLID de design
- **Domain-Driven Design**: Modelagem rica do domínio com entidades e eventos

## 🗄️ Banco de Dados

### Escolha Tecnológica - MySQL

O projeto utiliza **MySQL** como banco de dados principal pelas seguintes razões:

- **Familiaridade da Equipe**: O grupo possui maior experiência e conhecimento com MySQL, garantindo desenvolvimento mais eficiente e manutenção adequada
- **Maturidade**: MySQL é um banco consolidado e amplamente utilizado em aplicações empresariais
- **Performance**: Excelente performance para operações CRUD e consultas complexas
- **Suporte**: Ampla documentação e comunidade ativa
- **Compatibilidade**: Integração nativa com SQLAlchemy e frameworks Python

### Configurações de Conexão

- **Host**: mysql (dentro do Docker network) / localhost (acesso externo)
- **Porta**: 3306 (interna) / 3307 (externa para acesso local)
- **Database**: tech_challenge
- **Usuário**: tech_user
- **Senha**: tech_password

### Variáveis de Ambiente

```bash
DATABASE_URL=mysql+aiomysql://tech_user:tech_password@mysql:3306/tech_challenge
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=tech_challenge
MYSQL_USER=tech_user
MYSQL_PASSWORD=tech_password
SECRET_KEY=a4f8b9c2d3e4f567890abcdef1234567890abcdef1234567890abcdef12345678
```

### Acesso Externo ao MySQL

Para conectar ao MySQL a partir da sua máquina local (fora do Docker), use:
- **Host**: localhost
- **Porta**: 3307

Para usuários do DBeaver:

Clique com o botão direito na sua conexão, escolha "Editar Conexão"

Na tela "Configurações de conexão" (tela principal), clique em "Editar configurações do driver"

Clique em "Propriedades da conexão"

Clique com o botão direito na área "propriedades do usuário" e escolha "Adicionar nova propriedade"

Adicione duas propriedades: "useSSL" e "allowPublicKeyRetrieval"

Defina seus valores como "false" e "true" clicando duas vezes na coluna "value"

## 🔄 Migrations

As migrations são gerenciadas pelo Alembic:

```bash
# Criar nova migration
make migrate-create MSG="descrição da alteração"

# Aplicar migrations
make migrate-up

# Reverter última migration
make migrate-down

# Popular banco com dados fictícios (após aplicar migrations)
make populate-db
```

## 📚 API Endpoints (Exemplo)

### Clientes

- `GET /clientes/` - Listar todos os clientes
- `POST /clientes/` - Criar novo cliente
- `GET /clientes/{id}` - Obter cliente por ID
- `PUT /cliente/{id}` - Atualizar cliente existente
- `DELETE /cliente/{id}` - Deletar cliente existente
- `GET /clientes/cpf/{cpf}` - Obter cliente por CPF

### Exemplo de payload para criação/atualização de clientes:

```json
{
  "nome": "string",
  "telefone": "string",
  "email": "user@example.com",
  "cpf": "string"
}
```

## 🧪 Testes

Para executar os testes:

```bash
# Renomeie o arquivo "env-example" para ".env", com isso as informações necessárias para o teste serão carregadas.
# Usando Docker Compose diretamente
docker-compose exec app python -m pytest app/test/ -v

# Para testes utilizando FastAPI - Swagger UI, recomendamos a utilização do usuario padrão de ADMIN que possui acesso a todas as rotas.
# Os dados para login deste usuario se encontram em populate_db.py.
```

## 🔒 Segurança e Boas Práticas

- Uso de variáveis de ambiente para configurações sensíveis
- Conexões de banco de dados com pool de conexões
- Validação de dados com Pydantic
- Separação clara de responsabilidades seguindo arquitetura hexagonal
- Tratamento adequado de erros e exceções

## 🚧 Desenvolvimento

Para desenvolvimento local:

1. As alterações no código são refletidas automaticamente (hot reload)
2. Use `make logs` para acompanhar os logs da aplicação
3. Use `make shell` para acessar o container e executar comandos
4. Execute testes antes de fazer commits: `make test`