from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.services.signal_service import SignalService
from server.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/signals",
    tags=["Signals"],
)


@router.get("/running")
def get_running_signals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        return []

    signals = SignalService.get_running(db)

    return [
        {
            "id": signal.id,
            "public_id": signal.public_id,
            "magic_number": signal.magic_number,
            "symbol": signal.symbol,
            "action": signal.action,
            "status": signal.status,
            "created_at": signal.created_at,
        }
        for signal in signals
    ]


@router.get("/history")
def get_signal_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        return []

    signals = SignalService.get_history(db)

    return [
        {
            "id": signal.id,
            "public_id": signal.public_id,
            "magic_number": signal.magic_number,
            "symbol": signal.symbol,
            "action": signal.action,
            "status": signal.status,
            "created_at": signal.created_at,
            "closed_at": signal.closed_at,
        }
        for signal in signals
    ]