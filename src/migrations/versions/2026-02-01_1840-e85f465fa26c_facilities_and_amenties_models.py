"""facilities and amenties models

Revision ID: e85f465fa26c
Revises: cb82ff19b6f4
Create Date: 2026-02-01 18:40:35.120227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e85f465fa26c'
down_revision: Union[str, None] = '6740ddbc691e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'amenities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=False),
    )

    op.create_table(
        'room_amenities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('room_id', sa.Integer(), sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('amenity_id', sa.Integer(), sa.ForeignKey('amenities.id'), nullable=False),
    )

    op.create_table(
        'facilities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=False),
    )

    op.create_table(
        'room_facilities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('room_id', sa.Integer(), sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('facility_id', sa.Integer(), sa.ForeignKey('facilities.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('room_facilities')
    op.drop_table('facilities')
    op.drop_table('room_amenities')
    op.drop_table('amenities')