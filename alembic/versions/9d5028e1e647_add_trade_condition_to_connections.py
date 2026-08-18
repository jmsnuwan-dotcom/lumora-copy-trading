"""add trade condition to connections

Revision ID: 9d5028e1e647
Revises: ae9c9d2c2306
Create Date: 2026-08-18 20:48:30.959942

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9d5028e1e647"
down_revision: Union[str, Sequence[str], None] = "ae9c9d2c2306"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("connections")
    }

    if "trade_condition" not in columns:
        op.add_column(
            "connections",
            sa.Column(
                "trade_condition",
                sa.String(length=30),
                nullable=True,
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("connections")
    }

    if "trade_condition" in columns:
        op.drop_column(
            "connections",
            "trade_condition",
        )