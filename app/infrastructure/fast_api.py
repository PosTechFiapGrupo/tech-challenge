from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.container import Container
from app.infrastructure.database import database
from app.infrastructure.handlers import Handlers
from app.infrastructure.logging_config import get_logger, setup_logging
from app.infrastructure.middleware import (
    ObservabilityMiddleware,
    OrdemServicoMetricsMiddleware,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configurar logging estruturado
    setup_logging()
    logger.info("Application starting", extra={"event": "startup"})
    
    await app.container.init_resources()
    yield

    logger.info("Application shutting down", extra={"event": "shutdown"})
    await app.container.shutdown_resources()
    await database.close()


def create_app():
    fast_api = FastAPI(
        lifespan=lifespan,
        title="Tech Challenge API",
        description="API para gerenciamento de ordens de serviço de oficina mecânica",
        version="3.0.0",
    )
    
    fast_api.add_middleware(OrdemServicoMetricsMiddleware)
    fast_api.add_middleware(ObservabilityMiddleware)
    
    container = Container()
    fast_api.container = container
    container.wire(modules=list(Handlers.iterator()) + ["app.infrastructure.auth_dependencies"])

    for handler in Handlers.iterator():
        fast_api.include_router(handler.router)
    
    return fast_api
