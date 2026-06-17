"""Add a notes table

Revision ID: dc412abc9771
Revises: 6e93a7c74d71
Create Date: 2026-06-17 20:04:42.037365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc412abc9771'
down_revision: Union[str, Sequence[str], None] = '6e93a7c74d71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
