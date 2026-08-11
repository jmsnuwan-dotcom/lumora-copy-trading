from datetime import UTC, datetime

from sqlalchemy.orm import Session

from server.database.models import Connection
from server.schemas.connection import ConnectionCreate
from server.repositories.subscription_repository import SubscriptionRepository

class ConnectionService:

    @staticmethod
    def save(
        db: Session,
        request: ConnectionCreate,
    ) -> Connection:

        subscription = SubscriptionRepository.get_active_by_user(
            db=db,
            user_id=request.user_id,
        )

        if not subscription:
            raise ValueError(
                "No active subscription."
            )

        connection = (
            db.query(Connection)
            .filter(Connection.user_id == request.user_id)
            .first()
        )

        if connection:
            connection.mt5_login = request.mt5_login
            connection.mt5_password = request.mt5_password
            connection.mt5_server = request.mt5_server
            connection.status = "connected"
            connection.is_online = True
            connection.last_seen = datetime.now(UTC)

        else:
            connection = Connection(
                user_id=request.user_id,
                mt5_login=request.mt5_login,
                mt5_password=request.mt5_password,
                mt5_server=request.mt5_server,
                status="connected",
                is_online=True,
                last_seen=datetime.now(UTC),
            )

            db.add(connection)

        db.commit()
        db.refresh(connection)

        return connection

    @staticmethod
    def disconnect(
        db: Session,
        user_id: int,
    ) -> None:

        connection = (
            db.query(Connection)
            .filter(Connection.user_id == user_id)
            .first()
        )

        if not connection:
            return

        connection.status = "disconnected"
        connection.is_online = False
        connection.last_seen = datetime.now(UTC)

        db.commit()

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Connection)
            .filter(Connection.user_id == user_id)
            .first()
        )

    @staticmethod
    def heartbeat(
        db: Session,
        user_id: int,
    ):

        connection = (
            db.query(Connection)
            .filter(Connection.user_id == user_id)
            .first()
        )

        if not connection:
            return

        connection.last_seen = datetime.now(UTC)
        connection.is_online = True
        connection.status = "connected"

        db.commit()