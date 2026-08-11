from datetime import UTC, datetime

from server.database.models.signal_delivery import SignalDelivery
from server.repositories.signal_delivery_repository import SignalDeliveryRepository


class SignalDeliveryService:

    def __init__(self, repository: SignalDeliveryRepository):
        self.repository = repository

    def mark_received(
        self,
        delivery: SignalDelivery,
    ) -> SignalDelivery:

        delivery.status = "RECEIVED"
        delivery.received_at = datetime.now(UTC)

        return self.repository.update(delivery)

    def mark_executed(
        self,
        delivery: SignalDelivery,
        mt5_ticket: int,
    ) -> SignalDelivery:

        if delivery.status == "EXECUTED":
            raise ValueError(
                "Signal delivery has already been executed."
            )

        if delivery.status == "CLOSED":
            raise ValueError(
                "Signal delivery is already closed."
            )

        delivery.status = "EXECUTED"
        delivery.executed_at = datetime.now(UTC)
        delivery.mt5_ticket = mt5_ticket

        return self.repository.update(delivery)

    def mark_closed(
        self,
        delivery: SignalDelivery,
    ) -> SignalDelivery:

        delivery.status = "CLOSED"
        delivery.closed_at = datetime.now(UTC)

        return self.repository.update(delivery)
    
    def get_delivery(
        self,
        signal_id: int,
        user_id: int,
        connection_id: int,
    ) -> SignalDelivery | None:
        return self.repository.get_by_signal_user_connection(
            signal_id=signal_id,
            user_id=user_id,
            connection_id=connection_id,
        )