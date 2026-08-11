from datetime import UTC, datetime

from sqlalchemy.orm import Session

from server.database.models.signal import Signal


class SignalRepository:

    @staticmethod
    def create(
        db: Session,
        signal: Signal,
    ) -> Signal:

        db.add(signal)
        db.commit()
        db.refresh(signal)

        return signal

    @staticmethod
    def get_by_id(
        db: Session,
        signal_id: int,
    ) -> Signal | None:

        return (
            db.query(Signal)
            .filter(
                Signal.id == signal_id
            )
            .first()
        )

    @staticmethod
    def get_by_public_id(
        db: Session,
        public_id: str,
    ) -> Signal | None:

        return (
            db.query(Signal)
            .filter(
                Signal.public_id == public_id
            )
            .first()
        )

    @staticmethod
    def get_by_magic_number(
        db: Session,
        magic_number: int,
    ) -> Signal | None:

        return (
            db.query(Signal)
            .filter(
                Signal.magic_number
                == magic_number
            )
            .first()
        )

    @staticmethod
    def get_running(
        db: Session,
    ) -> list[Signal]:

        return (
            db.query(Signal)
            .filter(
                Signal.status == "RUNNING"
            )
            .order_by(
                Signal.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_history(
        db: Session,
    ) -> list[Signal]:

        return (
            db.query(Signal)
            .filter(
                Signal.status == "CLOSED"
            )
            .order_by(
                Signal.closed_at.desc()
            )
            .all()
        )

    @staticmethod
    def close(
        db: Session,
        signal: Signal,
    ) -> Signal:

        signal.status = "CLOSED"
        signal.closed_at = datetime.now(UTC)

        db.commit()
        db.refresh(signal)

        return signal