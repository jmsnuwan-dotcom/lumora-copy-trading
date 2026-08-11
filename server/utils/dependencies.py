from fastapi import Depends, HTTPException, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from server.database.db import SessionLocal, get_db
from server.database.models import Subscription, User
from server.utils.security import verify_access_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    try:
        payload = verify_access_token(
            credentials.credentials
        )

        user_id = int(
            payload["sub"]
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token.",
        )

    user = db.get(
        User,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found.",
        )

    return user


def require_active_subscription(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
) -> User:

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == current_user.id,
            Subscription.status == "ACTIVE",
        )
        .order_by(
            Subscription.id.desc()
        )
        .first()
    )

    if subscription is None:
        raise HTTPException(
            status_code=403,
            detail="Active subscription required.",
        )

    return current_user


async def get_current_user_ws(
    websocket: WebSocket,
):
    token = websocket.query_params.get(
        "token"
    )

    if not token:
        return None

    try:
        payload = verify_access_token(token)

        user_id = int(
            payload["sub"]
        )

    except Exception:
        return None

    db: Session = SessionLocal()

    try:
        user = db.get(
            User,
            user_id,
        )

        if not user:
            return None

        return user

    finally:
        db.close()