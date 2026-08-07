from sqlalchemy.orm import Session

from server.database.models import User


class UserService:

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(User)
            .order_by(User.id)
            .all()
        )

    @staticmethod
    def toggle_signals(
        db: Session,
        user_id: int,
    ):

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found.")

        user.signals_enabled = not user.signals_enabled

        db.commit()
        db.refresh(user)

        return user.signals_enabled