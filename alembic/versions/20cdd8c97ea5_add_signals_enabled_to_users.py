"""add signals_enabled to users

Revision ID: 20cdd8c97ea5
Revises: 5af16e845eba
Create Date: 2026-08-06
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20cdd8c97ea5"
down_revision: Union[str, Sequence[str], None] = "5af16e845eba"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "users",
        sa.Column(
            "signals_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

def downgrade() -> None:

    op.drop_column(
        "users",
        "signals_enabled",
    )