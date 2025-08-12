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

### 4. Acessar a aplicação

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

## 🗄️ Banco de Dados

O projeto usa MySQL como banco de dados principal com as seguintes configurações:

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

## 📁 Estrutura do Projeto

```
├── app/
│   ├── application/          # Camada de aplicação
│   │   ├── services/         # Serviços de aplicação
│   │   └── validators/       # Validadores
│   ├── domain/              # Camada de domínio
│   │   ├── entities/        # Entidades de domínio
│   │   ├── events/          # Eventos de domínio
│   │   ├── repositories/    # Interfaces dos repositórios
│   │   └── use_cases/       # Casos de uso
│   ├── infrastructure/      # Camada de infraestrutura
│   │   ├── handlers/        # Handlers HTTP (Controllers)
│   │   ├── models/          # Models do SQLAlchemy
│   │   ├── repositories/    # Implementações dos repositórios
│   │   └── schemas/         # Schemas Pydantic
│   └── test/               # Testes
├── migrations/             # Migrations do Alembic
├── docker-compose.yml      # Configuração Docker Compose
├── Dockerfile             # Dockerfile da aplicação
├── alembic.ini           # Configuração do Alembic
├── Makefile              # Comandos de automação
└── requirements.txt      # Dependências Python
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