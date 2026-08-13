import asyncio
import json
import logging

import httpx
import websockets

from client.config import API_URL
from client.services.connection_service import ConnectionService
from client.services.market_data_service import MarketDataService
from client.mt5.trade_executor import TradeExecutor


logger = logging.getLogger(__name__)


class WebSocketClient:

    def __init__(
        self,
        token: str,
        mt5_login: int,
        mt5_password: str,
        mt5_server: str,
    ) -> None:

        self.token = token
        self.mt5_login = mt5_login
        self.mt5_password = mt5_password
        self.mt5_server = mt5_server

        self.connection = None
        self.executor = TradeExecutor()

    # ==========================================================
    # MAIN START
    # ==========================================================

    async def start(self) -> None:

        print("WEBSOCKET START")

        market_data_task = asyncio.create_task(
            self._market_data_loop()
        )

        try:

            while True:

                try:

                    print("CALLING _RUN")

                    await self._run()

                except httpx.HTTPStatusError as e:

                    if e.response.status_code in (
                        401,
                        403,
                    ):

                        print(
                            "WEBSOCKET ACCESS DENIED:",
                            e.response.text,
                        )

                        logger.warning(
                            "WebSocket stopped: "
                            "subscription/access denied."
                        )

                        return

                    print(
                        "WEBSOCKET HTTP ERROR:",
                        repr(e),
                    )

                    logger.exception(
                        "WebSocket HTTP error."
                    )

                    await asyncio.sleep(5)

                except Exception as e:

                    print(
                        "WEBSOCKET ERROR:",
                        repr(e),
                    )

                    logger.exception(
                        "WebSocket client stopped."
                    )

                    await asyncio.sleep(5)

        finally:

            market_data_task.cancel()

            try:

                await market_data_task

            except asyncio.CancelledError:

                pass

    # ==========================================================
    # MARKET DATA LOOP
    # ==========================================================

    async def _market_data_loop(self) -> None:

        print("MARKET DATA LOOP STARTED")

        while True:

            try:

                MarketDataService.update_gold_price()

            except Exception:

                logger.exception(
                    "Market data update failed."
                )

            await asyncio.sleep(1)

    # ==========================================================
    # WEBSOCKET CONNECTION
    # ==========================================================

    async def _run(self) -> None:

        print("ENTER _RUN")

        logger.info(
            "Registering MT5 connection..."
        )

        print("CONNECT START")

        self.connection = (
            await ConnectionService.connect(
                token=self.token,
                mt5_login=self.mt5_login,
                mt5_password=self.mt5_password,
                mt5_server=self.mt5_server,
            )
        )

        logger.info(
            "Connection registered."
        )

        ws_url = (
            API_URL
            .replace(
                "http://",
                "ws://",
            )
            .replace(
                "https://",
                "wss://",
            )
            + f"/ws?token={self.token}"
        )

        logger.info(
            "Connecting: %s",
            ws_url,
        )

        print(
            "WS URL:",
            ws_url,
        )

        print(
            "BEFORE CONNECT"
        )

        async with websockets.connect(
            ws_url,
            ping_interval=20,
            ping_timeout=20,
        ) as websocket:

            print(
                "AFTER CONNECT"
            )

            logger.info(
                "WebSocket connected."
            )

            print(
                "WAITING FOR MESSAGE"
            )

            async for message in websocket:

                print(
                    "HANDLE MESSAGE:",
                    message,
                )

                print(
                    "RAW MESSAGE:",
                    message,
                )

                try:

                    data = json.loads(
                        message
                    )

                except json.JSONDecodeError:

                    logger.warning(
                        "Invalid message: %s",
                        message,
                    )

                    continue

                print(
                    "PARSED:",
                    data,
                )

                logger.info(
                    "Received: %s",
                    data,
                )

                await self.handle_message(
                    data
                )

    # ==========================================================
    # HANDLE SIGNAL
    # ==========================================================

    async def handle_message(
        self,
        message: dict,
    ) -> None:

        print(
            "HANDLE MESSAGE:",
            message,
        )

        action = message.get(
            "action"
        )

        print(
            "ACTION:",
            action,
        )

        if action not in {
            "BUY",
            "SELL",
            "CLOSE",
        }:

            logger.warning(
                "Unknown message: %s",
                message,
            )

            return

        print(
            "EXECUTING TRADE"
        )

        try:

            await self.executor.execute(
                message
            )

            logger.info(
                "%s executed successfully.",
                action,
            )

        except Exception:

            logger.exception(
                "Trade execution failed."
            )