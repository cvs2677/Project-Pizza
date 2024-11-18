"""Create total_price column for order column

Revision ID: c33f284273a1
Revises: 
Create Date: 2024-09-10 18:49:12.735342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c33f284273a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("order", sa.Column("total_price", sa.Float(), nullable=True))


def downgrade() -> None:
    pass
