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
        user_id: int,
    ):
        user = (
            db.query(User)
            .filter(User.id == user_id)
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

        subscription = Subscription(
            user_id=user_id,
            package_id=request.package_id,
            plan_id=request.plan_id,
            approved_by=None,
            status=request.status,
            payment_status="NOT_PAID",
            payment_slip=None,
            payment_submitted_at=None,
            start_date=None,
            end_date=None,
            is_trial=request.is_trial,
            trial_started_at=None,
            trial_ends_at=None,
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
                Subscription.status.in_(
                    [
                        "PENDING",
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

    @staticmethod
    def submit_payment(
        db: Session,
        user_id: int,
        payment_slip: str,
        is_trial: bool = False,
    ):
        now = datetime.now(UTC)

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
            )
            .order_by(Subscription.id.desc())
            .first()
        )

        if not subscription:
            raise ValueError(
                "No subscription found."
            )

        # ==========================================
        # FIRST PAYMENT
        # ==========================================

        if (
            subscription.status == "PENDING"
            and subscription.payment_status == "NOT_PAID"
        ):

            subscription.is_trial = is_trial

        # ==========================================
        # REMAINING 50% AFTER TRIAL
        # ==========================================

        elif (
            subscription.status == "EXPIRED"
            and subscription.is_trial
        ):

            if not subscription.trial_ends_at:
                raise ValueError(
                    "Trial expiration date not found."
                )

            trial_ends_at = subscription.trial_ends_at

            if trial_ends_at.tzinfo is None:
                trial_ends_at = trial_ends_at.replace(
                    tzinfo=UTC
                )

            if trial_ends_at > now:
                raise ValueError(
                    "Trial has not expired yet."
                )

        else:
            raise ValueError(
                "Payment cannot be submitted for this subscription."
            )

        if subscription.payment_status == "SUBMITTED":
            raise ValueError(
                "Payment has already been submitted."
            )

        subscription.payment_slip = payment_slip
        subscription.payment_status = "SUBMITTED"
        subscription.payment_submitted_at = now
        subscription.status = "PENDING"

        db.commit()
        db.refresh(subscription)

        return subscription
    @staticmethod
    def get_pending_payments(
        db: Session,
    ):
        return (
            db.query(Subscription)
            .options(
                joinedload(Subscription.user),
                joinedload(Subscription.package),
                joinedload(Subscription.plan),
            )
            .filter(
                Subscription.status == "PENDING",
                Subscription.payment_status == "SUBMITTED",
            )
            .order_by(Subscription.payment_submitted_at.desc())
            .all()
        )


    @staticmethod
    def approve_payment(
        db: Session,
        subscription_id: int,
        admin_id: int,
    ):
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.id == subscription_id,
                Subscription.status == "PENDING",
                Subscription.payment_status == "SUBMITTED",
            )
            .first()
        )

        if not subscription:
            raise ValueError(
                "Pending payment not found."
            )

        user = (
            db.query(User)
            .filter(
                User.id == subscription.user_id
            )
            .first()
        )

        if not user:
            raise ValueError(
                "User not found."
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

        now = datetime.now(UTC)

        # ==========================================
        # FIRST PAYMENT → START 24H TRIAL
        # ==========================================

        if (
            subscription.is_trial
            and subscription.trial_started_at is None
        ):

            subscription.trial_started_at = now
            subscription.trial_ends_at = (
                now + timedelta(hours=24)
            )

            # Normal package must NOT start yet.
            subscription.start_date = None
            subscription.end_date = None

            subscription.status = "ACTIVE"
            subscription.payment_status = "APPROVED"
            subscription.approved_by = admin_id

            user.status = "active"
            user.is_active = True

        # ==========================================
        # REMAINING 50% → START NORMAL PACKAGE
        # ==========================================

        elif (
            subscription.is_trial
            and subscription.trial_ends_at is not None
        ):

            trial_ends_at = subscription.trial_ends_at

            if trial_ends_at.tzinfo is None:
                trial_ends_at = trial_ends_at.replace(
                    tzinfo=UTC
                )

            if trial_ends_at > now:
                raise ValueError(
                    "Trial has not expired yet."
                )

            end_date = None

            if plan.duration_days:
                end_date = now + timedelta(
                    days=plan.duration_days
                )

            subscription.is_trial = False
            subscription.trial_started_at = None
            subscription.trial_ends_at = None

            subscription.status = "ACTIVE"
            subscription.payment_status = "APPROVED"
            subscription.approved_by = admin_id

            subscription.start_date = now
            subscription.end_date = end_date

            user.status = "active"
            user.is_active = True

        # ==========================================
        # NORMAL EXISTING PAYMENT
        # ==========================================

        else:

            subscription.is_trial = False
            subscription.status = "APPROVED"
            subscription.payment_status = "APPROVED"
            subscription.approved_by = admin_id
            subscription.start_date = None
            subscription.end_date = None

            user.status = "active"
            user.is_active = True

        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def give_trial(
        db: Session,
        subscription_id: int,
        admin_id: int,
    ):
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.id == subscription_id,
                Subscription.status == "APPROVED",
                Subscription.payment_status == "APPROVED",
                Subscription.is_trial == False,
            )
            .first()
        )

        if not subscription:
            raise ValueError(
                "Active paid subscription not found."
            )

        user = (
            db.query(User)
            .filter(User.id == subscription.user_id)
            .first()
        )

        if not user:
            raise ValueError(
                "User not found."
            )

        plan = (
            db.query(Plan)
            .filter(Plan.id == subscription.plan_id)
            .first()
        )

        if not plan:
            raise ValueError(
                "Plan not found."
            )

        now = datetime.now(UTC)

        # Normal package must NOT start during trial.
        package_start = None
        package_end = None

        subscription.start_date = package_start
        subscription.end_date = package_end

        subscription.is_trial = True
        subscription.trial_started_at = now
        subscription.trial_ends_at = (
            now + timedelta(hours=24)
        )

        subscription.approved_by = admin_id

        # Normal package starts after the 24-hour trial.
        subscription.start_date = package_start
        subscription.end_date = package_end

        subscription.status = "ACTIVE"
        subscription.payment_status = "APPROVED"

        user.status = "active"
        user.is_active = True

        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def activate_package(
        db: Session,
        subscription_id: int,
        admin_id: int,
    ):
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.id == subscription_id,
                Subscription.status == "APPROVED",
                Subscription.payment_status == "APPROVED",
                Subscription.is_trial == False,
            )
            .first()
        )

        if not subscription:
            raise ValueError(
                "Approved package not found."
            )

        plan = (
            db.query(Plan)
            .filter(Plan.id == subscription.plan_id)
            .first()
        )

        if not plan:
            raise ValueError(
                "Plan not found."
            )

        now = datetime.now(UTC)

        end_date = None

        if plan.duration_days:
            end_date = now + timedelta(
                days=plan.duration_days
            )

        subscription.status = "ACTIVE"
        subscription.is_trial = False
        subscription.approved_by = admin_id
        subscription.start_date = now
        subscription.end_date = end_date

        user = (
            db.query(User)
            .filter(User.id == subscription.user_id)
            .first()
        )

        if not user:
            raise ValueError(
                "User not found."
            )

        user.status = "active"
        user.is_active = True

        db.commit()
        db.refresh(subscription)

        return subscription

    @staticmethod
    def get_admin_clients(
        db: Session,
    ):
        return (
            db.query(Subscription)
            .options(
                joinedload(Subscription.user),
                joinedload(Subscription.package),
                joinedload(Subscription.plan),
            )
            .join(User, Subscription.user_id == User.id)
            .filter(
                User.role == "user",
            )
            .order_by(User.id.desc())
            .all()
        )

    @staticmethod
    def process_expired_trials(
        db: Session,
    ) -> None:

        now = datetime.now(UTC)

        subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "ACTIVE",
                Subscription.is_trial == True,
                Subscription.trial_ends_at.isnot(None),
            )
            .all()
        )

        changed = False

        for subscription in subscriptions:

            trial_ends_at = subscription.trial_ends_at

            if trial_ends_at.tzinfo is None:
                trial_ends_at = trial_ends_at.replace(
                    tzinfo=UTC
                )

            if trial_ends_at > now:
                continue

            # Trial expired.
            # Keep is_trial=True so the system knows
            # remaining 50% payment is required.

            subscription.status = "EXPIRED"

            subscription.trial_started_at = None

            changed = True

            print(
                "TRIAL EXPIRED - REMAINING PAYMENT REQUIRED:",
                subscription.user_id,
                subscription.package_id,
            )

        if changed:
            db.commit()
    @staticmethod
    def process_expired_packages(
        db: Session,
    ) -> None:

        now = datetime.now(UTC)

        subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "ACTIVE",
                Subscription.is_trial == False,
                Subscription.end_date.isnot(None),
            )
            .all()
        )

        changed = False

        for subscription in subscriptions:

            end_date = subscription.end_date

            if end_date.tzinfo is None:
                end_date = end_date.replace(
                    tzinfo=UTC
                )

            if end_date >= now:
                continue

            subscription.status = "EXPIRED"

            changed = True

            print(
                "PACKAGE EXPIRED:",
                subscription.user_id,
                subscription.package_id,
            )

        if changed:
            db.commit()

    @staticmethod
    def get_active_subscribers(
        db: Session,
        admin_id: int,
    ):

        SubscriptionService.process_expired_trials(
            db=db,
        )

        SubscriptionService.process_expired_packages(
            db=db,
        )

        now = datetime.now(UTC)

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

        active_subscribers = []

        for subscription in subscriptions:

            user = subscription.user
            package = subscription.package

            if user is None:
                continue

            if package is None:
                continue

            if user.role != "user":
                continue

            if not user.is_active:
                continue

            if not user.signals_enabled:
                continue

            if not package.is_active:
                continue

            # ------------------------------------------
            # 24H TRIAL
            # ------------------------------------------

            if subscription.is_trial:

                if not subscription.trial_ends_at:
                    continue

                trial_ends_at = subscription.trial_ends_at

                if trial_ends_at.tzinfo is None:
                    trial_ends_at = trial_ends_at.replace(
                        tzinfo=UTC
                    )

                if trial_ends_at <= now:
                    continue

                # ==========================================
                # 24H TRIAL SETTINGS
                # ==========================================

                active_subscribers.append(
                    subscription
                )

                continue

            # ------------------------------------------
            # NORMAL PAID PACKAGE
            # ------------------------------------------

            if not subscription.start_date:
                continue

            start_date = subscription.start_date

            if start_date.tzinfo is None:
                start_date = start_date.replace(
                    tzinfo=UTC
                )

            if start_date > now:
                continue

            if subscription.end_date:

                end_date = subscription.end_date

                if end_date.tzinfo is None:
                    end_date = end_date.replace(
                        tzinfo=UTC
                    )

                if end_date < now:
                    continue

            active_subscribers.append(
                subscription
            )

        print(
            "ACTIVE SIGNAL SUBSCRIBERS:",
            len(active_subscribers),
        )

        for subscription in active_subscribers:
            print(
                "USER:",
                subscription.user_id,
                "PACKAGE:",
                subscription.package.name,
                "TRADES:",
                subscription.package.trades_per_signal,
                "LOT:",
                subscription.package.lot_size,
                "TRIAL:",
                subscription.is_trial,
            )

        return active_subscribers

    @staticmethod
    def get_by_id(
        db: Session,
        subscription_id: int,
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.id == subscription_id
            )
            .first()
        )