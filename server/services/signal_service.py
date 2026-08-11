import secrets

from server.database.models.signal import Signal
from server.repositories.signal_repository import SignalRepository


class SignalService:

    @staticmethod
    def generate_magic_number(db) -> int:

        for _ in range(20):

            magic_number = secrets.randbelow(
                900_000_000
            ) + 100_000_000

            existing = SignalRepository.get_by_magic_number(
                db=db,
                magic_number=magic_number,
            )

            if existing is None:
                return magic_number

        raise RuntimeError(
            "Unable to generate unique magic number."
        )

    @staticmethod
    def create_signal(
        db,
        symbol: str,
        action: str,
    ) -> Signal:

        if action not in {"BUY", "SELL"}:
            raise ValueError(
                "Signal action must be BUY or SELL."
            )

        magic_number = (
            SignalService.generate_magic_number(
                db=db,
            )
        )

        signal = Signal(
            magic_number=magic_number,
            symbol=symbol,
            action=action,
            status="RUNNING",
        )

        return SignalRepository.create(
            db=db,
            signal=signal,
        )

    @staticmethod
    def get_running(db) -> list[Signal]:

        return SignalRepository.get_running(
            db=db,
        )

    @staticmethod
    def get_history(db) -> list[Signal]:

        return SignalRepository.get_history(
            db=db,
        )

    @staticmethod
    def get_by_id(
        db,
        signal_id: int,
    ) -> Signal | None:

        return SignalRepository.get_by_id(
            db=db,
            signal_id=signal_id,
        )

    @staticmethod
    def get_by_magic_number(
        db,
        magic_number: int,
    ) -> Signal | None:

        return SignalRepository.get_by_magic_number(
            db=db,
            magic_number=magic_number,
        )

    @staticmethod
    def close_signal(
        db,
        signal: Signal,
    ) -> Signal:

        if signal.status != "RUNNING":
            raise ValueError(
                "Signal is already closed."
            )

        return SignalRepository.close(
            db=db,
            signal=signal,
        )