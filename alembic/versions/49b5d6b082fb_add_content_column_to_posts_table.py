"""add content column to posts table

Revision ID: 49b5d6b082fb
Revises: d2aa38bfc90f
Create Date: 2024-07-06 10:22:27.503814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49b5d6b082fb'
down_revision: Union[str, None] = 'd2aa38bfc90f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
