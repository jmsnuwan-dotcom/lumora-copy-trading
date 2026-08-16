from datetime import UTC, datetime

from sqlalchemy.orm import Session

from server.database.models import (
    Connection,
    Package,
    Plan,
    Subscription,
    User,
)
from server.services.subscription_service import (
    SubscriptionService,
)


class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        user_id: int,
    ):

        SubscriptionService.process_expired_trials(
            db=db,
        )

        SubscriptionService.process_expired_packages(
            db=db,
        )

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status.in_(
                    [
                        "APPROVED",
                        "ACTIVE",
                    ]
                ),
            )
            .order_by(
                Subscription.id.desc()
            )
            .first()
        )

        if not subscription:
            raise ValueError(
                "No subscription found."
            )

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise ValueError(
                "User not found."
            )

        package = (
            db.query(Package)
            .filter(
                Package.id == subscription.package_id
            )
            .first()
        )

        if not package:
            raise ValueError(
                "Package not found."
            )

        plan = (
            db.query(Plan)
            .filter(
                Plan.id == subscription.plan_id
            )
            .first()
        )

        if not plan:
            raise ValueError(
                "Plan not found."
            )

        connection = (
            db.query(Connection)
            .filter(
                Connection.user_id == user_id
            )
            .first()
        )

        connection_status = "Offline"
        mt5_login = None
        mt5_server = None
        last_seen = None
        client_version = None

        if connection:
            connection_status = (
                "Online"
                if connection.is_online
                else "Offline"
            )

            mt5_login = connection.mt5_login
            mt5_server = connection.mt5_server
            last_seen = connection.last_seen
            client_version = (
                connection.client_version
                or connection.app_version
            )

        remaining_days = None

        # Trial is separate from the normal paid package.
        # Do not show paid package remaining days during trial.
        if subscription.is_trial:
            remaining_days = None

        else:
            if subscription.end_date:
                now = datetime.now(UTC)

                end_date = subscription.end_date

                if end_date.tzinfo is None:
                    end_date = end_date.replace(
                        tzinfo=UTC
                    )

                remaining_days = (
                    end_date - now
                ).days

                if remaining_days < 0:
                    remaining_days = 0

        signals_enabled = False

        if (
            user.is_active
            and user.signals_enabled
            and package.is_active
        ):

            if subscription.status == "ACTIVE":

                if subscription.is_trial:

                    if subscription.trial_ends_at:

                        trial_ends_at = (
                            subscription.trial_ends_at
                        )

                        if (
                            trial_ends_at.tzinfo
                            is None
                        ):
                            trial_ends_at = (
                                trial_ends_at.replace(
                                    tzinfo=UTC
                                )
                            )

                        if (
                            trial_ends_at
                            > datetime.now(UTC)
                        ):
                            signals_enabled = True

                else:

                    if subscription.start_date:

                        start_date = (
                            subscription.start_date
                        )

                        if (
                            start_date.tzinfo
                            is None
                        ):
                            start_date = (
                                start_date.replace(
                                    tzinfo=UTC
                                )
                            )

                        now = datetime.now(UTC)

                        if start_date <= now:

                            if subscription.end_date:

                                end_date = (
                                    subscription.end_date
                                )

                                if (
                                    end_date.tzinfo
                                    is None
                                ):
                                    end_date = (
                                        end_date.replace(
                                            tzinfo=UTC
                                        )
                                    )

                                if end_date >= now:
                                    signals_enabled = True

                            else:
                                signals_enabled = True

        return {
            "full_name": user.full_name,
            "email": user.email,

            "package": package.name,
            "plan": plan.name,
            "lot_size": (
                0.01
                if subscription.is_trial
                else float(package.lot_size)
            ),

            "trade_copies": (
                1
                if subscription.is_trial
                else int(package.trades_per_signal)
            ),

            "status": subscription.status,
            "is_active": user.is_active,

            "start_date": subscription.start_date,
            "expire_date": subscription.end_date,

            "is_trial": subscription.is_trial,
            "trial_ends_at": subscription.trial_ends_at,

            "connection_status": connection_status,
            "mt5_login": mt5_login,
            "mt5_server": mt5_server,
            "last_seen": last_seen,
            "client_version": client_version,

            "balance": None,
            "equity": None,
            "open_trades": None,

            "remaining_days": remaining_days,

            "signals_enabled": signals_enabled,
        }