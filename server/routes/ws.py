from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.database.db import SessionLocal
from server.database.models import Subscription
from server.services.connection_service import ConnectionService
from server.trading.websocket_manager import websocket_manager
from server.utils.dependencies import get_current_user_ws


router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
):
    user = await get_current_user_ws(
        websocket
    )

    if user is None:
        await websocket.close(
            code=1008
        )
        return

    db = SessionLocal()

    try:

        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user.id,
                Subscription.status == "ACTIVE",
            )
            .order_by(
                Subscription.id.desc()
            )
            .first()
        )

        if not subscription:
            await websocket.close(
                code=1008
            )
            return

        await websocket_manager.connect(
            user.id,
            websocket,
        )

        while True:

            try:

                await websocket.receive_text()

            except WebSocketDisconnect:

                break

    except Exception:

        raise

    finally:

        try:

            await websocket_manager.disconnect(
                user.id,
                websocket,
            )

        finally:

            ConnectionService.disconnect(
                db=db,
                user_id=user.id,
            )

            db.close()