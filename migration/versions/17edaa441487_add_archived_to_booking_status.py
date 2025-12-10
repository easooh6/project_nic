"""add ARCHIVED to booking_status

Revision ID: 17edaa441487
Revises: 422a209ee617
Create Date: 2025-12-10 19:22:29.543644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17edaa441487'
down_revision: Union[str, Sequence[str], None] = '422a209ee617'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE bookingstatus ADD VALUE 'ARCHIVED'")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
