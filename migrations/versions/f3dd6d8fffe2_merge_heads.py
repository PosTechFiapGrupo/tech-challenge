"""Merge heads

Revision ID: f3dd6d8fffe2
Revises: 15bbe7e1474a, e1fb419a7cbd
Create Date: 2025-08-11 02:20:08.730918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3dd6d8fffe2'
down_revision = ('15bbe7e1474a', 'e1fb419a7cbd')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
