"""add package price

Revision ID: ec154cd204fa
Revises: 25ec8e42b09b
Create Date: 2026-08-13 07:19:35.469099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec154cd204fa'
down_revision: Union[str, Sequence[str], None] = '25ec8e42b09b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "packages",
        sa.Column(
            "price",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0.00",
        ),
    )


def downgrade() -> None:
    op.drop_column("packages", "price")
