from sqlalchemy.orm import Session

from server.database.models import User
from server.repositories.user_repository import UserRepository
from server.utils.security import hash_password, verify_password
from server.database.models import Subscription
from server.repositories.subscription_repository import SubscriptionRepository
from datetime import UTC, datetime

class AuthService:

    @staticmethod
    def register(
        db: Session,
        full_name: str,
        email: str,
        phone_number: str,
        password: str,
        confirm_password: str,
        package_id: int,
        plan_id: int,
    ):

        if UserRepository.get_by_email(db, email):
            raise ValueError("Email already exists.")

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role="user",
            status="pending_payment",
            is_active=False,
            trial_used=False,
            phone_number=phone_number,
        )

        created_user = UserRepository.create(db, user)

        subscription = Subscription(
            user_id=created_user.id,
            package_id=package_id,
            plan_id=plan_id,
            status="PENDING",
            approved_by=1,
            start_date=datetime.now(UTC),
            end_date=None,
        )

        SubscriptionRepository.create(
            db=db,
            subscription=subscription,
        )

        return created_user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):

        user = UserRepository.get_by_email(db, email)

        if not user:
            return None

        ok = verify_password(password, user.password_hash)

        if not ok:
            return None
        
        if (
            user.role != "admin"
            and (
                user.status != "active"
                or not user.is_active
            )
        ):
            raise ValueError(
                "Your account is waiting for payment approval."
            )

        return user