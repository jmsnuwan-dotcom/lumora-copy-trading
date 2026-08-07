from fastapi import APIRouter, Depends

from server.utils.dependencies import get_current_user
from server.services.online_client_registry import OnlineClientRegistry
from server.database.db import get_db
from sqlalchemy.orm import Session
from server.services.connection_service import ConnectionService

router = APIRouter(
    prefix="/heartbeat",
    tags=["Heartbeat"],
)


@router.post("")
def heartbeat(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    OnlineClientRegistry.heartbeat(current_user.id)

    ConnectionService.heartbeat(
        db=db,
        user_id=current_user.id,
    )

    return {
        "success": True,
    }