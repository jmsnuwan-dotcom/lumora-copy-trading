"""add payment settings

Revision ID: f25f35abc135
Revises: a816ccc1021c
Create Date: 2026-08-08 18:58:51.933780

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "f25f35abc135"
down_revision: Union[str, Sequence[str], None] = "a816ccc1021c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "payment_settings" in inspector.get_table_names():
        return

    op.create_table(
        "payment_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bank_name", sa.String(length=100), nullable=False),
        sa.Column("account_name", sa.String(length=150), nullable=False),
        sa.Column("account_number", sa.String(length=100), nullable=False),
        sa.Column("branch", sa.String(length=100), nullable=False),
        sa.Column("bank_instructions", sa.String(length=500), nullable=False),
        sa.Column("crypto_currency", sa.String(length=20), nullable=False),
        sa.Column("crypto_network", sa.String(length=50), nullable=False),
        sa.Column("crypto_address", sa.String(length=255), nullable=False),
        sa.Column("crypto_instructions", sa.String(length=500), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_payment_settings_id"),
        table_name="payment_settings",
    )

    op.drop_table("payment_settings")