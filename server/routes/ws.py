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
async def websocket_endpoint(websocket: WebSocket):
    print("WS CONNECT")
    print("QUERY:", dict(websocket.query_params))

    user = await get_current_user_ws(websocket)

    if user is None:
        print("AUTH FAILED")
        await websocket.close(code=1008)
        return

    db = SessionLocal()

    try:
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user.id,
                Subscription.status == "ACTIVE",
            )
            .order_by(Subscription.id.desc())
            .first()
        )

        if not subscription:
            print(
                "WS ACCESS DENIED: "
                "NO ACTIVE SUBSCRIPTION"
            )

            await websocket.close(code=1008)
            return

        print("=" * 60)
        print("WS USER ID :", user.id)
        print("WS EMAIL   :", user.email)
        print("WS ROLE    :", user.role)
        print(
            "WS SUBSCRIPTION :",
            subscription.status,
        )
        print("=" * 60)

        await websocket_manager.connect(
            user.id,
            websocket,
        )

        print("CONNECTION ACCEPTED")

        while True:
            try:
                message = await websocket.receive_text()
                print("WS MESSAGE:", message)

            except WebSocketDisconnect as e:
                print(
                    f"WS DISCONNECTED: {e.code}"
                )
                break

    except Exception as e:
        print("WS ERROR:", repr(e))
        raise

    finally:
        print("WS FINALLY")

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