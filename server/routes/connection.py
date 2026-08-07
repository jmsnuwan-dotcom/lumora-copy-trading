from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.user import User
from server.schemas.connection import (
    ConnectionCreate,
    ConnectionResponse,
)
from server.services.connection_service import ConnectionService
from server.utils.dependencies import get_current_user
from fastapi import HTTPException

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
    current_user: User = Depends(get_current_user),
):
    request.user_id = current_user.id

    return ConnectionService.save(
        db=db,
        request=request,
    )

@router.get(
    "/me",
    response_model=ConnectionResponse,
)
def get_my_connection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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