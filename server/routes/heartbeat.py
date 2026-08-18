from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
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


class HeartbeatRequest(BaseModel):
    balance: Optional[float] = None
    equity: Optional[float] = None
    trade_condition: Optional[str] = None


@router.post("")
def heartbeat(
    data: HeartbeatRequest,
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
        balance=data.balance,
        equity=data.equity,
        trade_condition=data.trade_condition,
    )

    return {
        "success": True,
    }