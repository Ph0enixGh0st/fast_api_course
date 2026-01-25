"""price -> price_per_night

Revision ID: 6740ddbc691e
Revises: 6e2c78897200
Create Date: 2026-01-25 14:13
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6740ddbc691e'
down_revision: Union[str, None] = '6e2c78897200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('bookings', sa.Column('price_per_night', sa.Integer(), nullable=True))
    op.execute('UPDATE bookings SET price_per_night = price WHERE price IS NOT NULL')
    op.alter_column('bookings', 'price_per_night', nullable=False)
    op.drop_column('bookings', 'price')


def downgrade() -> None:
    op.add_column('bookings', sa.Column('price', sa.Integer(), nullable=True))
    op.execute('UPDATE bookings SET price = price_per_night WHERE price_per_night IS NOT NULL')
    op.alter_column('bookings', 'price', nullable=False)
    op.drop_column('bookings', 'price_per_night')