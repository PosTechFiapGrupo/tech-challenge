# ---- Build Stage ----
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt pyproject.toml ./
COPY alembic.ini ./
COPY migrations ./migrations/
COPY populate_db.py ./

# Install dependencies
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# ---- Final Stage ----
FROM python:3.12-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser alembic.ini .
COPY --chown=appuser:appuser migrations ./migrations/
COPY --chown=appuser:appuser populate_db.py .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start the application with gunicorn
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "app.main:application"]
