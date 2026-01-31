"""rename price to price_per_night

Revision ID: cb82ff19b6f4
Revises: 50380fc449c0
Create Date: 2026-01-31 18:50:23.252871

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb82ff19b6f4"
down_revision: Union[str, None] = "50380fc449c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
