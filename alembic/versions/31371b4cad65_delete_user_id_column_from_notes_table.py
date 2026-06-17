"""Delete user_id column from notes table

Revision ID: 31371b4cad65
Revises: dc412abc9771
Create Date: 2026-06-17 21:11:09.253175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31371b4cad65'
down_revision: Union[str, Sequence[str], None] = 'dc412abc9771'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
