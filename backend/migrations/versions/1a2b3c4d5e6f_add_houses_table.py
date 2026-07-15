"""Add houses table and house_id to rooms

Revision ID: 1a2b3c4d5e6f
Revises: 96b6ad7ec059
Create Date: 2026-07-15 05:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a2b3c4d5e6f'
down_revision: Union[str, Sequence[str], None] = '96b6ad7ec059'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create houses table
    op.create_table('houses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_houses_id'), 'houses', ['id'], unique=False)

    # Add house_id to rooms
    op.add_column('rooms', sa.Column('house_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_rooms_house_id_houses', 'rooms', 'houses', ['house_id'], ['id'])


def downgrade() -> None:
    # Remove house_id from rooms
    op.drop_constraint('fk_rooms_house_id_houses', 'rooms', type_='foreignkey')
    op.drop_column('rooms', 'house_id')

    # Drop houses table
    op.drop_index(op.f('ix_houses_id'), table_name='houses')
    op.drop_table('houses')
