from sqlalchemy.orm import Session

from server.services.signal_service import SignalService
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
        magic_number: int | None = None,
    ) -> None:

        if action not in {"BUY", "SELL", "CLOSE"}:
            raise ValueError(
                "Invalid trade action."
            )

        # ==================================================
        # BUY / SELL
        # ==================================================

        if action in {"BUY", "SELL"}:

            signal = SignalService.create_signal(
                db=db,
                symbol=symbol,
                action=action,
            )

            magic_number = signal.magic_number

            print("=" * 60)
            print("NEW SIGNAL CREATED")
            print("SIGNAL ID :", signal.id)
            print("ACTION    :", signal.action)
            print("SYMBOL    :", signal.symbol)
            print("MAGIC     :", signal.magic_number)
            print("STATUS    :", signal.status)
            print("=" * 60)

        # ==================================================
        # CLOSE
        # ==================================================

        else:

            if magic_number is None:
                raise ValueError(
                    "Magic number is required for CLOSE."
                )

            signal = SignalService.get_by_magic_number(
                db=db,
                magic_number=magic_number,
            )

            if signal is None:
                raise ValueError(
                    "Running signal not found."
                )

            if signal.status != "RUNNING":
                raise ValueError(
                    "Signal is already closed."
                )

            print("=" * 60)
            print("CLOSING SIGNAL")
            print("SIGNAL ID :", signal.id)
            print("ACTION    :", signal.action)
            print("SYMBOL    :", signal.symbol)
            print("MAGIC     :", signal.magic_number)
            print("=" * 60)

        # ==================================================
        # GET ACTIVE SUBSCRIBERS
        # ==================================================

        subscriptions = (
            SubscriptionService.get_active_subscribers(
                db=db,
                admin_id=admin_id,
            )
        )

        print("=" * 60)
        print("ADMIN:", admin_id)
        print("ACTION:", action)
        print("SIGNAL MAGIC:", magic_number)
        print(
            "SUBSCRIPTIONS:",
            len(subscriptions),
        )
        print("=" * 60)

        sent_count = 0

        # ==================================================
        # SEND TO CLIENTS
        # ==================================================

        for subscription in subscriptions:

            user = subscription.user

            print(
                "SUB:",
                user.id,
                subscription.status,
                subscription.approved_by,
            )

            if not user.is_active:
                print(
                    "SKIP USER - ACCOUNT DEACTIVATED:",
                    user.id,
                )
                continue

            if not user.signals_enabled:
                print(
                    "SKIP USER - SIGNALS OFF:",
                    user.id,
                )
                continue

            online = await websocket_manager.is_online(
                user.id
            )

            print(
                "ONLINE:",
                user.id,
                online,
            )

            if not online:
                print(
                    "SKIP USER - OFFLINE:",
                    user.id,
                )
                continue

            package = subscription.package

            if package is None:
                print(
                    "SKIP USER - NO PACKAGE:",
                    user.id,
                )
                continue

            # ==================================================
            # TRIAL / NORMAL SETTINGS
            # ==================================================

            if subscription.is_trial:
                trade_lot_size = 0.01
                trade_copies = 1
            else:
                trade_lot_size = float(
                    package.lot_size
                )
                trade_copies = int(
                    package.trades_per_signal
                )

            # ==================================================
            # CLIENT MESSAGE
            # ==================================================

            message = {
                "action": action,
                "trade_id": trade_id,
                "magic_number": magic_number,
                "symbol": symbol,
                "lot_size": trade_lot_size,
                "trade_copies": trade_copies,
            }

            print("=" * 60)
            print("SENDING TRADE")
            print("USER        :", user.id)
            print("EMAIL       :", user.email)
            print("PACKAGE     :", package.name)
            print("TRIAL       :", subscription.is_trial)
            print("LOT SIZE    :", trade_lot_size)
            print("TRADE COPIES:", trade_copies)
            print("MAGIC       :", magic_number)
            print("MESSAGE     :", message)
            print("=" * 60)

            await websocket_manager.send(
                user_id=user.id,
                message=message,
            )

            sent_count += 1

            print(
                "MESSAGE SENT TO:",
                user.id,
            )

        # ==================================================
        # CLOSE SIGNAL IN DATABASE
        # ==================================================

        if action == "CLOSE":

            SignalService.close_signal(
                db=db,
                signal=signal,
            )

            print("=" * 60)
            print("SIGNAL CLOSED")
            print("SIGNAL ID :", signal.id)
            print("MAGIC     :", signal.magic_number)
            print("SENT TO   :", sent_count)
            print("=" * 60)

        else:

            print("=" * 60)
            print("SIGNAL DELIVERY COMPLETE")
            print("SIGNAL ID :", signal.id)
            print("MAGIC     :", signal.magic_number)
            print("SENT TO   :", sent_count)
            print("=" * 60)