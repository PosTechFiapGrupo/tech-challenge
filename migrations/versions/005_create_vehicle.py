"""create vehicles table

Revision ID: 6ffc06aa6890
Revises: 001_initial
Create Date: 2025-08-03 15:07:54.147685
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005_create_vehicle'
down_revision = '004_create_inventory_itens'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('license_plate', sa.String(length=20), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    
    op.execute("""
        INSERT INTO vehicles (brand, model, year, license_plate) VALUES
        ('Toyota', 'Corolla', 2020, 'ABC1D23'),
        ('Honda', 'Civic', 2019, 'XYZ9W87');
    """)

def downgrade() -> None:
    op.drop_table('vehicles')
