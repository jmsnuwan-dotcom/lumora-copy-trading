from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database.db import Base


class SignalDelivery(Base):
    __tablename__ = "signal_deliveries"

    __table_args__ = (
        UniqueConstraint(
            "signal_id",
            "user_id",
            "connection_id",
            name="uq_signal_delivery_signal_user_connection",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    signal_id: Mapped[int] = mapped_column(
        ForeignKey("signals.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    connection_id: Mapped[int] = mapped_column(
        ForeignKey("connections.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
    )

    mt5_ticket: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    executed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    signal = relationship(
        "Signal",
        foreign_keys=[signal_id],
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
    )

    connection = relationship(
        "Connection",
        foreign_keys=[connection_id],
    )