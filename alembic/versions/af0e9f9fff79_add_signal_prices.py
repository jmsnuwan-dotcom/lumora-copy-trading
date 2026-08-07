"""add_signal_prices

Revision ID: af0e9f9fff79
Revises: 48a37d885ca4
Create Date: 2026-07-29 07:24:21.174273
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "af0e9f9fff79"
down_revision: Union[str, Sequence[str], None] = "48a37d885ca4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "signals",
        sa.Column(
            "entry_price",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "signals",
        sa.Column(
            "stop_loss",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "signals",
        sa.Column(
            "take_profit",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "signals",
        sa.Column(
            "comment",
            sa.String(length=100),
            nullable=True,
        ),
    )


def downgrade() -> None:

    op.drop_column("signals", "comment")
    op.drop_column("signals", "take_profit")
    op.drop_column("signals", "stop_loss")
    op.drop_column("signals", "entry_price")