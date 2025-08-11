from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.container import Container
from app.infrastructure.database import database
from app.infrastructure.handlers import Handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await app.container.init_resources()
    yield

    await app.container.shutdown_resources()
    await database.close()

def create_app():
    fast_api = FastAPI(lifespan=lifespan)
    container = Container()
    fast_api.container = container
    container.wire(modules=list(Handlers.iterator()) + ["app.infrastructure.auth_dependencies"])

    for handler in Handlers.iterator():
        fast_api.include_router(handler.router)
    return fast_api
