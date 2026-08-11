from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.user import User
from server.schemas.connection import (
    ConnectionCreate,
    ConnectionResponse,
)
from server.services.connection_service import ConnectionService
from server.utils.dependencies import require_active_subscription


router = APIRouter(
    prefix="/connections",
    tags=["Connections"],
)


@router.post(
    "",
    response_model=ConnectionResponse,
)
def save_connection(
    request: ConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_active_subscription
    ),
):
    request.user_id = current_user.id

    try:
        return ConnectionService.save(
            db=db,
            request=request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=ConnectionResponse,
)
def get_my_connection(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_active_subscription
    ),
):
    connection = ConnectionService.get_by_user(
        db=db,
        user_id=current_user.id,
    )

    if connection is None:
        raise HTTPException(
            status_code=404,
            detail="Connection not found.",
        )

    return connection