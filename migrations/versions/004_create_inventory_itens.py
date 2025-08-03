"""Initial migration - create inventory_items and vehicles tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-26 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004_create_inventory_itens'
down_revision = '003_create_servicos'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Criar tabela inventory_items
     op.create_table(
        'inventory_items',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('minimum_stock', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('unit_price', sa.Float(), nullable=False),
    )

    op.execute("""
        INSERT INTO inventory_items (name, description, quantity, minimum_stock, unit_price) VALUES
        ('Pastilha de Freio', 'Pastilha de freio dianteira para vários carros', 50, 10, 35.50),
        ('Óleo de Motor', 'Óleo sintético 5W-30, 1 litro', 100, 20, 25.00);
    """)


def downgrade() -> None:
    op.drop_table('inventory_items')
