from server.database.models.subscription import Subscription


class SubscriptionRepository:

    @staticmethod
    def get_active_by_user(
        db,
        user_id: int,
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
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