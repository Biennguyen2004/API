"""null is true

Revision ID: 7409c281b91e
Revises: 451fe1ef12cc
Create Date: 2024-07-06 17:32:22.447688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7409c281b91e'
down_revision: Union[str, None] = '451fe1ef12cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
