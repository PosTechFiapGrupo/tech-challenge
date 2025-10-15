import os, sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# garante que o pacote app/ esteja no sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ✅ Base sem side effects
from app.infrastructure.database import Base

# ✅ imports explícitos de TODOS os models
from app.infrastructure.models.user_model import UserModel
from app.infrastructure.models.cliente import ClienteModel
from app.infrastructure.models.vehicle_model import VehicleModel
from app.infrastructure.models.servico import ServicoModel
from app.infrastructure.models.inventory_item_model import InventoryItemModel
from app.infrastructure.models.ordem_servico import OrdemServicoModel
from app.infrastructure.models.ordem_servico_servico import OrdemServicoServicoModel
from app.infrastructure.models.ordem_servico_inventory_item import OrdemServicoInventoryItemModel

target_metadata = Base.metadata

def get_database_url():
    # 1ª preferência: MIGRATION_DATABASE_URL (síncrona/pymysql)
    url = os.getenv("MIGRATION_DATABASE_URL")
    if not url:
        # 2ª: DATABASE_URL, mas força pymysql se vier aiomysql
        url = os.getenv("DATABASE_URL", "mysql+pymysql://tech_user:tech_password@mysql:3306/tech_challenge")
    return url.replace("aiomysql", "pymysql")

def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
