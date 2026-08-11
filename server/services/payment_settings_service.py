from sqlalchemy.orm import Session

from server.database.models import PaymentSettings
from server.schemas.payment_settings import PaymentSettingsUpdate


class PaymentSettingsService:

    @staticmethod
    def get(db: Session):

        settings = (
            db.query(PaymentSettings)
            .order_by(PaymentSettings.id.asc())
            .first()
        )

        if settings is None:
            settings = PaymentSettings(
                bank_name="",
                account_name="",
                account_number="",
                branch="",
                bank_instructions="",
                crypto_currency="USDT",
                crypto_network="",
                crypto_address="",
                crypto_instructions="",
            )

            db.add(settings)
            db.commit()
            db.refresh(settings)

        return settings

    @staticmethod
    def update(
        db: Session,
        request: PaymentSettingsUpdate,
    ):

        settings = PaymentSettingsService.get(db)

        settings.bank_name = request.bank_name.strip()
        settings.account_name = request.account_name.strip()
        settings.account_number = request.account_number.strip()
        settings.branch = request.branch.strip()
        settings.bank_instructions = request.bank_instructions.strip()

        settings.crypto_currency = request.crypto_currency.strip()
        settings.crypto_network = request.crypto_network.strip()
        settings.crypto_address = request.crypto_address.strip()
        settings.crypto_instructions = (
            request.crypto_instructions.strip()
        )

        db.commit()
        db.refresh(settings)

        return settings