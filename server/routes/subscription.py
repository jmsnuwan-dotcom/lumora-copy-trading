from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.user import User
from server.database.models.subscription import Subscription
from server.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
)
from server.services.subscription_service import SubscriptionService
from server.utils.dependencies import get_current_user

from server.schemas.payment_settings import PaymentSettingsResponse
from server.services.payment_settings_service import PaymentSettingsService


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    response_model=SubscriptionResponse,
)
def create_subscription(
    request: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return SubscriptionService.create(
            db=db,
            request=request,
            user_id=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[SubscriptionResponse],
)
def get_subscriptions(
    db: Session = Depends(get_db),
):
    return SubscriptionService.get_all(db)


@router.get(
    "/payment-settings",
    response_model=PaymentSettingsResponse,
)
def get_payment_settings(
    db: Session = Depends(get_db),
):
    return PaymentSettingsService.get(db)


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
    "/payment",
    response_model=SubscriptionResponse,
)
async def submit_payment(
    slip: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf",
    }

    extension = Path(
        slip.filename or ""
    ).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only JPG, JPEG, PNG, and PDF "
                "files are allowed."
            ),
        )

    payment_dir = Path(
        "storage/payment_slips"
    )

    payment_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = (
        f"{uuid4().hex}{extension}"
    )

    file_path = (
        payment_dir / filename
    )

    try:
        with file_path.open("wb") as buffer:
            while chunk := await slip.read(
                1024 * 1024
            ):
                buffer.write(chunk)

        return SubscriptionService.submit_payment(
            db=db,
            user_id=current_user.id,
            payment_slip=str(file_path),
        )

    except ValueError as e:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )