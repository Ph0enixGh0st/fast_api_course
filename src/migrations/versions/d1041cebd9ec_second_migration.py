"""Second migration

Revision ID: d1041cebd9ec
Revises: 
Create Date: 2025-05-11 13:41:39.010608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1041cebd9ec'
down_revision: Union[str, None] = 'd1041cebd9eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('hotel_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['hotel_id'],
            ['hotels.id']
        )
)


def downgrade() -> None:
    op.drop_table('rooms')

