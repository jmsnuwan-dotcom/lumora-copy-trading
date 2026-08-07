from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
)
from server.services.subscription_service import SubscriptionService
from server.database.models.user import User
from server.utils.dependencies import get_current_user

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
):

    try:
        return SubscriptionService.create(
            db=db,
            request=request,
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
    "/me",
    response_model=SubscriptionResponse,
)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    subscription = SubscriptionService.get_active_by_user(
        db,
        current_user.id,
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="No active subscription.",
        )

    return subscription