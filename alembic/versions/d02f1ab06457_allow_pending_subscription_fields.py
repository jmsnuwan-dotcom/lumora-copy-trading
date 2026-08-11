"""allow pending subscription fields

Revision ID: d02f1ab06457
Revises: 9a5da0f8cbd4
Create Date: 2026-08-08

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.

revision: str = "d02f1ab06457"
down_revision: Union[str, Sequence[str], None] = "9a5da0f8cbd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("subscriptions") as batch_op:
        batch_op.alter_column(
            "approved_by",
            nullable=True,
        )

        batch_op.alter_column(
            "start_date",
            nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("subscriptions") as batch_op:
        batch_op.alter_column(
            "approved_by",
            nullable=False,
        )

        batch_op.alter_column(
            "start_date",
            nullable=False,
        )