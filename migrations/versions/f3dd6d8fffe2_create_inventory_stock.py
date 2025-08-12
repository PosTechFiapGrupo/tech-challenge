"""Merge heads + cria inventory_movements

Revision ID: f3dd6d8fffe2
Revises: 15bbe7e1474a, e1fb419a7cbd
Create Date: 2025-08-11 02:20:08.730918
"""
from alembic import op
import sqlalchemy as sa

# Identificadores da revisão
revision = "f3dd6d8fffe2"
down_revision = ("15bbe7e1474a", "e1fb419a7cbd")  # ✅ precisa ser tupla com TODAS as heads
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "inventory_movements",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("inventory_items.id"), nullable=False, index=True),
        sa.Column("os_id", sa.String(36), nullable=True),
        sa.Column("type", sa.Enum("ENTRADA", "SAIDA", "AJUSTE", name="inv_mov_type"), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("note", sa.String(255)),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        mysql_engine="InnoDB", mysql_charset="utf8mb4",
    )

def downgrade():
    op.drop_table("inventory_movements")
    # ❌ Não usar DROP TYPE no MySQL; o Enum é por coluna.
