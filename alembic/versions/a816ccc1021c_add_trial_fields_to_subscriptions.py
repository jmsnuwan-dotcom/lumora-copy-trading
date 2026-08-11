"""add trial fields to subscriptions

Revision ID: a816ccc1021c
Revises: d02f1ab06457
Create Date: 2026-08-08 12:17:01.759892

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a816ccc1021c"
down_revision: Union[str, Sequence[str], None] = "d02f1ab06457"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "subscriptions",
        sa.Column(
            "is_trial",
            sa.Boolean(),
            server_default="0",
            nullable=False,
        ),
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "trial_started_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "trial_ends_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "subscriptions",
        "trial_ends_at",
    )

    op.drop_column(
        "subscriptions",
        "trial_started_at",
    )

    op.drop_column(
        "subscriptions",
        "is_trial",
    )