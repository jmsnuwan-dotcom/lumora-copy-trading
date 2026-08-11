from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.services.connection_service import ConnectionService
from server.services.online_client_registry import (
    OnlineClientRegistry,
)
from server.utils.dependencies import require_active_subscription


router = APIRouter(
    prefix="/heartbeat",
    tags=["Heartbeat"],
)


@router.post("")
def heartbeat(
    current_user=Depends(
        require_active_subscription
    ),
    db: Session = Depends(get_db),
):
    OnlineClientRegistry.heartbeat(
        current_user.id
    )

    ConnectionService.heartbeat(
        db=db,
        user_id=current_user.id,
    )

    return {
        "success": True,
    }