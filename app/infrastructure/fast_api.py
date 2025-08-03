from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.handlers import inventory_item_handler
from app.infrastructure.handlers import Handlers
from app.infrastructure.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await database.close()


def create_app():
    fast_api = FastAPI(lifespan=lifespan)
    for handler in Handlers.iterator():
        fast_api.include_router(handler.router)
        fast_api.include_router(inventory_item_handler.router)
    return fast_api
