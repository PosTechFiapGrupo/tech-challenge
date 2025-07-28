FROM python:3.12-slim

# Instalar dependências do sistema necessárias para MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt pyproject.toml ./
COPY alembic.ini ./
COPY migrations ./migrations/

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ./app ./app

EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:application", "--reload", "--host", "0.0.0.0", "--port", "8000"]