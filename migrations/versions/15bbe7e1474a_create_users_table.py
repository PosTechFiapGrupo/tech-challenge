"""create users table

Revision ID: 15bbe7e1474a
Revises: 5c689865e085
Create Date: 2025-08-09 00:38:00.101554
"""

from passlib.context import CryptContext
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '15bbe7e1474a'
down_revision = '5c689865e085'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), primary_key=True, index=True),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('funcao', sa.String(length=100), nullable=False),
        sa.Column('criado_em', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('users')
