from sqlalchemy.orm import Session

from server.database.models.signal_delivery import SignalDelivery


class SignalDeliveryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        delivery: SignalDelivery,
    ) -> SignalDelivery:

        self.db.add(delivery)
        self.db.commit()
        self.db.refresh(delivery)

        return delivery

    def get_by_id(
        self,
        delivery_id: int,
    ) -> SignalDelivery | None:

        return (
            self.db.query(SignalDelivery)
            .filter(
                SignalDelivery.id == delivery_id,
            )
            .first()
        )

    def get_by_signal_user_connection(
        self,
        signal_id: int,
        user_id: int,
        connection_id: int,
    ) -> SignalDelivery | None:

        return (
            self.db.query(SignalDelivery)
            .filter(
                SignalDelivery.signal_id == signal_id,
                SignalDelivery.user_id == user_id,
                SignalDelivery.connection_id == connection_id,
            )
            .first()
        )

    def update(
        self,
        delivery: SignalDelivery,
    ) -> SignalDelivery:

        self.db.commit()
        self.db.refresh(delivery)

        return delivery