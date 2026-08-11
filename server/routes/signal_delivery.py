from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.repositories.signal_delivery_repository import SignalDeliveryRepository
from server.services.signal_delivery_service import SignalDeliveryService
from server.schemas.signal_delivery import SignalExecutedRequest
from server.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/signal-deliveries",
    tags=["Signal Deliveries"],
)


@router.post("/executed")
def mark_executed(
    data: SignalExecutedRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    repository = SignalDeliveryRepository(db)
    service = SignalDeliveryService(repository)

    delivery = repository.get_by_id(
        data.delivery_id
    )

    if delivery is None:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found",
        )

    if delivery.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Delivery does not belong to this user.",
        )

    try:
        service.mark_executed(
            delivery=delivery,
            mt5_ticket=data.mt5_ticket,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    return {
        "success": True,
    }