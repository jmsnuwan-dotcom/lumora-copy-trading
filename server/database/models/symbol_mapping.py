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


class SymbolMapping(Base):
    __tablename__ = "symbol_mappings"

    __table_args__ = (
        UniqueConstraint(
            "connection_id",
            "master_symbol",
            name="uq_connection_master_symbol",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    connection_id: Mapped[int] = mapped_column(
        ForeignKey("connections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    master_symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    broker_symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    connection = relationship(
        "Connection",
        back_populates="symbol_mappings",
    )