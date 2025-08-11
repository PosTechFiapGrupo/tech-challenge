import os
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from app.infrastructure.fast_api import create_app

load_dotenv()

@pytest.fixture(scope="function", autouse=True)
def configure_test_env():
    os.environ.setdefault("SECRET_KEY", "5a2c7f6d8e934ab99d8f7c9b1c4e2a7f58c1d3e6b9a48f0c2f7e1d8c4b6a9e3f")
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
    print("\n[TEST SETUP] Variáveis de ambiente configuradas para testes.")

@pytest.fixture(scope="function")
def app():
    return create_app()

@pytest.fixture(scope="function")
async def async_client(app):
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def auth_headers(async_client):
    login_data = {
        "username": "admin@test.com",
        "password": "senha123"
    }
    response = await async_client.post("/auth/token", data=login_data)
    assert response.status_code == 200, f"Falha ao autenticar: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
