from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.user import User
from server.database.models.subscription import Subscription
from server.schemas.subscription import SubscriptionResponse
from server.schemas.payment_settings import (
    PaymentSettingsResponse,
    PaymentSettingsUpdate,
)
from server.schemas.admin_client import AdminClientResponse
from server.services.subscription_service import (
    SubscriptionService,
)
from server.services.payment_settings_service import (
    PaymentSettingsService,
)
from server.services.user_service import UserService
from server.utils.dependencies import get_current_user

from server.database.models.connection import Connection


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required.",
        )

    return current_user


@router.get(
    "/payments/pending",
)
def get_pending_payments(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    subscriptions = (
        SubscriptionService.get_pending_payments(db)
    )

    payments = []

    for subscription in subscriptions:

        # ==================================================
        # PAYMENT TYPE
        # ==================================================

        if (
            subscription.is_trial
            and subscription.trial_ends_at is None
        ):
            payment_type = "24H Trial - First Payment"

        elif (
            subscription.is_trial
            and subscription.trial_ends_at is not None
        ):
            payment_type = "Remaining Payment"

        else:
            payment_type = "Normal Payment"

        # ==================================================
        # PACKAGE PRICE
        # ==================================================

        full_package_price = subscription.plan.price

        # ==================================================
        # AMOUNT PAID
        # ==================================================

        if payment_type in {
            "24H Trial - First Payment",
            "Remaining Payment",
        }:
            amount_paid = full_package_price / 2

        else:
            amount_paid = full_package_price

        # ==================================================
        # RESPONSE
        # ==================================================

        payments.append(
            {
                "id": subscription.id,
                "user_id": subscription.user_id,
                "full_name": subscription.user.full_name,
                "email": subscription.user.email,
                "phone_number": subscription.user.phone_number,

                "package": subscription.package.name,
                "plan": subscription.plan.name,
                "duration_days": (
                    subscription.plan.duration_days
                ),

                "payment_type": payment_type,
                "amount_paid": amount_paid,
                "full_package_price": full_package_price,

                "payment_status": (
                    subscription.payment_status
                ),

                "payment_slip": (
                    subscription.payment_slip
                ),

                "payment_submitted_at": (
                    subscription.payment_submitted_at
                ),
            }
        )

    return payments

@router.post(
    "/payments/{subscription_id}/approve",
    response_model=SubscriptionResponse,
)
def approve_payment(
    subscription_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        return SubscriptionService.approve_payment(
            db=db,
            subscription_id=subscription_id,
            admin_id=admin.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/clients",
    response_model=list[AdminClientResponse],
)

def get_admin_clients(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    subscriptions = (
        SubscriptionService.get_admin_clients(db)
    )

    results = []

    for subscription in subscriptions:

        connection = (
            db.query(Connection)
            .filter(
                Connection.user_id == subscription.user.id
            )
            .first()
        )

        results.append(
            {
                "id": subscription.user.id,
                "subscription_id": subscription.id,
                "full_name": subscription.user.full_name,
                "email": subscription.user.email,
                "phone_number": subscription.user.phone_number,

                "status": subscription.status,
                "is_active": subscription.user.is_active,

                "package": (
                    subscription.package.name
                    if subscription.package
                    else None
                ),
                "plan": (
                    subscription.plan.name
                    if subscription.plan
                    else None
                ),
                "payment_status": (
                    subscription.payment_status
                ),

                "is_trial": subscription.is_trial,
                "trial_ends_at": (
                    subscription.trial_ends_at
                ),

                "start_date": subscription.start_date,
                "end_date": subscription.end_date,

                # ==================================================
                # TRADE MONITOR
                # ==================================================

                "is_online": (
                    connection.is_online
                    if connection
                    else False
                ),

                "balance": (
                    connection.balance
                    if connection
                    else None
                ),

                "equity": (
                    connection.equity
                    if connection
                    else None
                ),

                "trade_condition": (
                    connection.trade_condition
                    if connection
                    else None
                ),

                "last_seen": (
                    connection.last_seen
                    if connection
                    else None
                ),
            }
        )

    return results

@router.get(
    "/payments/{subscription_id}/slip",
)
def view_payment_slip(
    subscription_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    subscription = SubscriptionService.get_by_id(
        db=db,
        subscription_id=subscription_id,
    )

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Payment not found.",
        )

    if not subscription.payment_slip:
        raise HTTPException(
            status_code=404,
            detail="Payment slip not found.",
        )

    file_path = Path(
        subscription.payment_slip
    )

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Payment slip file not found.",
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
    )


@router.get(
    "/me",
    response_model=SubscriptionResponse,
)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
        )
        .order_by(
            Subscription.id.desc()
        )
        .first()
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="No subscription found.",
        )

    return subscription


@router.post(
    "/trial/{subscription_id}",
    response_model=SubscriptionResponse,
)
def give_trial(
    subscription_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        return SubscriptionService.give_trial(
            db=db,
            subscription_id=subscription_id,
            admin_id=admin.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/package/{subscription_id}/activate",
    response_model=SubscriptionResponse,
)
def activate_package(
    subscription_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        return SubscriptionService.activate_package(
            db=db,
            subscription_id=subscription_id,
            admin_id=admin.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.put(
    "/clients/{user_id}/active"
)
def toggle_client_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    try:
        enabled = UserService.toggle_active(
            db=db,
            user_id=user_id,
        )

        return {
            "is_active": enabled,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get(
    "/payment-settings",
    response_model=PaymentSettingsResponse,
)
def get_payment_settings(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return PaymentSettingsService.get(db)


@router.put(
    "/payment-settings",
    response_model=PaymentSettingsResponse,
)
def update_payment_settings(
    request: PaymentSettingsUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return PaymentSettingsService.update(
        db=db,
        request=request,
    )