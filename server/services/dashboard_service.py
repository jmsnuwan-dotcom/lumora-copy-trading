from datetime import datetime

from sqlalchemy.orm import Session

from server.database.models import (
    Connection,
    Package,
    Plan,
    Subscription,
    User,
)


class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int,
    ):

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
            )
            .first()
        )

        if not subscription:
            raise ValueError("No active subscription.")

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        package = (
            db.query(Package)
            .filter(Package.id == subscription.package_id)
            .first()
        )

        plan = (
            db.query(Plan)
            .filter(Plan.id == subscription.plan_id)
            .first()
        )

        connection = (
            db.query(Connection)
            .filter(Connection.user_id == user_id)
            .first()
        )

        connection_status = "Offline"

        if connection and connection.is_online:
            connection_status = "Online"

        remaining_days = None

        if subscription.end_date:
            now = datetime.utcnow()

            remaining_days = (
                subscription.end_date - now
            ).days

            if remaining_days < 0:
                remaining_days = 0

        return {
            "full_name": user.full_name,
            "email": user.email,
            "package": package.name,
            "plan": plan.name,
            "lot_size": float(package.lot_size),
            "status": subscription.status,
            "expire_date": subscription.end_date,
            "connection_status": connection_status,
            "remaining_days": remaining_days,
            "balance": None,
            "equity": None,
            "open_trades": None,
            "signals_enabled": user.signals_enabled,
        }