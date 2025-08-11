"""create users table

Revision ID: 15bbe7e1474a
Revises: 004_create_vehicle
Create Date: 2025-08-09 00:38:00.101554
"""

from passlib.context import CryptContext
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '15bbe7e1474a'
down_revision = '004_create_vehicle'
branch_labels = None
depends_on = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('funcao', sa.String(length=100), nullable=False),
        sa.Column('criado_em', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    hash1 = pwd_context.hash("123456")
    hash2 = pwd_context.hash("123456")
    hash3 = pwd_context.hash("123456")

    op.execute(f"""
        INSERT INTO users (nome, email, hashed_password, funcao) VALUES
        ('Jose Silva', 'jose@teste.com', '{hash1}', 'cliente'),
        ('Carlos Miguel', 'carlos@teste.com', '{hash2}', 'mecanico'),
        ('Maria Clara', 'maria@teste.com', '{hash3}', 'atendente');
    """)


def downgrade() -> None:
    op.drop_table('users')
