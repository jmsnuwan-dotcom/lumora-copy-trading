from datetime import UTC, datetime

from server.database.models.subscription import Subscription


class SubscriptionRepository:

    ...

    @staticmethod
    def get_active_by_user(db, user_id: int):

        now = datetime.now(UTC)

        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
                Subscription.start_date <= now,
                (
                    (Subscription.end_date == None)
                    | (Subscription.end_date >= now)
                ),
            )
            .first()
        )

    @staticmethod
    def create(
        db,
        subscription: Subscription,
    ):

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        return subscription