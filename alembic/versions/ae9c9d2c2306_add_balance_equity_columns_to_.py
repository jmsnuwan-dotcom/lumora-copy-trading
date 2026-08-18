"""add balance equity columns to connections

Revision ID: ae9c9d2c2306
Revises: 12130e23f2ef
Create Date: 2026-08-18
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ae9c9d2c2306"
down_revision: Union[str, Sequence[str], None] = "12130e23f2ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("connections")
    }

    if "balance" not in columns:
        op.add_column(
            "connections",
            sa.Column(
                "balance",
                sa.Float(),
                nullable=True,
            ),
        )

    if "equity" not in columns:
        op.add_column(
            "connections",
            sa.Column(
                "equity",
                sa.Float(),
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

    if "equity" in columns:
        op.drop_column("connections", "equity")

    if "balance" in columns:
        op.drop_column("connections", "balance")