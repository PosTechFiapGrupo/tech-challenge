"""Initial migration - create products and inventory_items tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-26 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import CHAR

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Criar tabela inventory_items
    op.create_table(
        'inventory_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False, default=0),
    )


def downgrade() -> None:
    op.drop_table('inventory_items')
