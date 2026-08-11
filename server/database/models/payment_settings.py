from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.database.db import Base


class PaymentSettings(Base):
    __tablename__ = "payment_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    bank_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
    )

    account_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        default="",
    )

    account_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
    )

    branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
    )

    bank_instructions: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
    )

    crypto_currency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="USDT",
    )

    crypto_network: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="",
    )

    crypto_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="",
    )

    crypto_instructions: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )