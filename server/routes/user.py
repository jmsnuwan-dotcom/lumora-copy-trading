from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.database.models.user import User
from server.schemas.user import UserResponse
from server.services.user_service import UserService
from server.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):

    return UserService.get_all(db)


@router.put("/signals")
def toggle_signals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("USER ID:", current_user.id)

    try:
        enabled = UserService.toggle_signals(
            db=db,
            user_id=current_user.id,
        )

        print("NEW VALUE:", enabled)

        return {
            "signals_enabled": enabled,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )