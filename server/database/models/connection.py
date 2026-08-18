from datetime import UTC, datetime
import uuid

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database.db import Base
from sqlalchemy import Boolean


class Connection(Base):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    public_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    mt5_login: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    mt5_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    mt5_server: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    client_id: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    computer_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    windows_user: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    app_version: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_online: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="0",
        nullable=False,
    )

    balance: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    equity: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    client_version: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    trade_condition: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    symbol_mappings = relationship(
        "SymbolMapping",
        back_populates="connection",
        cascade="all, delete-orphan",
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
    )