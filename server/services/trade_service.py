from sqlalchemy.orm import Session

from server.services.subscription_service import SubscriptionService
from server.trading.websocket_manager import websocket_manager


class TradeService:

    @staticmethod
    async def send_trade(
        db: Session,
        admin_id: int,
        action: str,
        symbol: str,
        trade_id: str,
        magic_number: int,
    ) -> None:

        subscriptions = SubscriptionService.get_active_subscribers(
            db=db,
            admin_id=admin_id,
        )

        print("=" * 60)
        print("ADMIN:", admin_id)
        print("SUBSCRIPTIONS:", len(subscriptions))
        print("=" * 60)

        for subscription in subscriptions:

            print(
                "SUB:",
                subscription.user_id,
                subscription.status,
                subscription.approved_by,
            )

            user = subscription.user

            online = await websocket_manager.is_online(user.id)

            print("ONLINE:", user.id, online)

            if not online:
                continue

            message = {
                "action": action,
                "trade_id": trade_id,
                "magic_number": magic_number,
                "symbol": symbol,
                "lot_size": float(subscription.package.lot_size),
                "trade_copies": subscription.package.trades_per_signal,
            }

            print("MESSAGE:", message)

            print("=" * 60)
            print("SENDING TO USER :", user.id)
            print("EMAIL           :", user.email)
            print("MESSAGE         :", message)
            print("=" * 60)

            await websocket_manager.send(
                user_id=user.id,
                message=message,
            )

            print("MESSAGE SENT TO:", user.id)

        print("=" * 60)