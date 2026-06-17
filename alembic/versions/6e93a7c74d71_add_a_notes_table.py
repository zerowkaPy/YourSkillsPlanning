"""Add a notes table

Revision ID: 6e93a7c74d71
Revises: 0f107585b5d3
Create Date: 2026-06-17 20:04:16.954370

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e93a7c74d71'
down_revision: Union[str, Sequence[str], None] = '0f107585b5d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
