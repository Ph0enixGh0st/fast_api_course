"""price_per_night update

Revision ID: 50380fc449c0
Revises: 6740ddbc691e
Create Date: 2026-01-31 18:45:27.574184

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50380fc449c0"
down_revision: Union[str, None] = "6740ddbc691e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
