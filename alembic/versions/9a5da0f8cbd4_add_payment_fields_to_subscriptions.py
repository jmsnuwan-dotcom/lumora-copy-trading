"""add payment fields to subscriptions

Revision ID: 9a5da0f8cbd4
Revises: 20cdd8c97ea5
Create Date: 2026-08-08 09:08:03.515643

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "9a5da0f8cbd4"
down_revision: Union[str, Sequence[str], None] = "20cdd8c97ea5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "subscriptions",
        sa.Column(
            "payment_status",
            sa.String(length=20),
            nullable=False,
            server_default="NOT_PAID",
        ),
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "payment_slip",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "subscriptions",
        sa.Column(
            "payment_submitted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "subscriptions",
        "payment_submitted_at",
    )

    op.drop_column(
        "subscriptions",
        "payment_slip",
    )

    op.drop_column(
        "subscriptions",
        "payment_status",
    )