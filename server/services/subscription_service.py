from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session, joinedload

from server.database.models import (
    Package,
    Plan,
    Subscription,
    User,
)


class SubscriptionService:

    @staticmethod
    def get_all(
        db: Session,
    ):
        return (
            db.query(Subscription)
            .order_by(Subscription.id)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        request,
    ):

        user = (
            db.query(User)
            .filter(User.id == request.user_id)
            .first()
        )

        if not user:
            raise ValueError("User not found.")

        package = (
            db.query(Package)
            .filter(Package.id == request.package_id)
            .first()
        )

        if not package:
            raise ValueError("Package not found.")

        plan = (
            db.query(Plan)
            .filter(Plan.id == request.plan_id)
            .first()
        )

        if not plan:
            raise ValueError("Plan not found.")

        start_date = datetime.now(UTC)

        end_date = None

        if plan.duration_days:
            end_date = start_date + timedelta(
                days=plan.duration_days
            )

        subscription = Subscription(
            user_id=request.user_id,
            package_id=request.package_id,
            plan_id=request.plan_id,
            approved_by=request.approved_by,
            status=request.status,
            start_date=start_date,
            end_date=end_date,
        )

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def get_active_by_user(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(Subscription)
            .options(
                joinedload(Subscription.package),
                joinedload(Subscription.plan),
            )
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
            )
            .first()
        )

    @staticmethod
    def get_active_subscribers(
        db: Session,
        admin_id: int,
    ):

        subscriptions = (
            db.query(Subscription)
            .options(
                joinedload(Subscription.user),
                joinedload(Subscription.package),
                joinedload(Subscription.plan),
            )
            .filter(
                Subscription.approved_by == admin_id,
                Subscription.status == "ACTIVE",
            )
            .all()
        )

        print("SUBSCRIPTIONS:", len(subscriptions))

        for s in subscriptions:
            print(
                s.user_id,
                s.status,
                s.approved_by,
            )

        return subscriptions