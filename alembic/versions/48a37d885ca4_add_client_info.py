"""add_client_info

Revision ID: 48a37d885ca4
Revises: 0a8aa917bbe2
Create Date: 2026-07-28 23:12:10.678109
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "48a37d885ca4"
down_revision: Union[str, Sequence[str], None] = "0a8aa917bbe2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "connections",
        sa.Column("client_id", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "connections",
        sa.Column("computer_name", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "connections",
        sa.Column("windows_user", sa.String(length=100), nullable=True),
    )

    op.add_column(
        "connections",
        sa.Column("app_version", sa.String(length=20), nullable=True),
    )

    op.add_column(
        "connections",
        sa.Column(
            "is_online",
            sa.Boolean(),
            nullable=False,
            server_default="0",
        ),
    )

    # SQLite doesn't support ALTER TABLE ADD CONSTRAINT.
    # We'll create the unique constraint later when using PostgreSQL.


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("connections", "is_online")
    op.drop_column("connections", "app_version")
    op.drop_column("connections", "windows_user")
    op.drop_column("connections", "computer_name")
    op.drop_column("connections", "client_id")