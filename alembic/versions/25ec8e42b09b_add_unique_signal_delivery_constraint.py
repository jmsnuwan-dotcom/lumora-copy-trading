"""add unique signal delivery constraint

Revision ID: 25ec8e42b09b
Revises: f25f35abc135
Create Date: 2026-08-11 08:17:51.018626

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "25ec8e42b09b"
down_revision: Union[str, Sequence[str], None] = "f25f35abc135"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    constraints = inspector.get_unique_constraints("signal_deliveries")

    existing_names = {
        constraint["name"]
        for constraint in constraints
    }

    if "uq_signal_delivery_signal_user_connection" in existing_names:
        return

    with op.batch_alter_table("signal_deliveries") as batch_op:
        batch_op.create_unique_constraint(
            "uq_signal_delivery_signal_user_connection",
            [
                "signal_id",
                "user_id",
                "connection_id",
            ],
        )


def downgrade() -> None:

    with op.batch_alter_table(
        "signal_deliveries"
    ) as batch_op:

        batch_op.drop_constraint(
            "uq_signal_delivery_signal_user_connection",
            type_="unique",
        )