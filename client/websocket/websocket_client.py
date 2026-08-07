import asyncio
import json
import logging

import websockets

from client.config import (
    API_URL,
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
)
from client.services.connection_service import ConnectionService
from client.mt5.trade_executor import TradeExecutor


logger = logging.getLogger(__name__)


class WebSocketClient:

    def __init__(self, token: str) -> None:

        self.token = token
        self.connection = None
        self.executor = TradeExecutor()

    async def start(self) -> None:

        print("WEBSOCKET START")

        while True:
            try:
                print("CALLING _RUN")
                await self._run()

            except Exception as e:
                print("WEBSOCKET ERROR:", repr(e))
                logger.exception("WebSocket client stopped.")
                await asyncio.sleep(5)

    async def _run(self) -> None:

        print("ENTER _RUN")
        logger.info("Logging in...")

        print("CONNECT START")

        self.connection = await ConnectionService.connect(
            token=self.token,
            mt5_login=MT5_LOGIN,
            mt5_password=MT5_PASSWORD,
            mt5_server=MT5_SERVER,
        )

        logger.info("Connection registered.")

        ws_url = (
            API_URL.replace("http://", "ws://")
            .replace("https://", "wss://")
            + f"/ws?token={self.token}"
        )

        logger.info("Connecting: %s", ws_url)

        print("WS URL:", ws_url)
        print("BEFORE CONNECT")

        async with websockets.connect(
            ws_url,
            ping_interval=20,
            ping_timeout=20,
        ) as websocket:

            print("AFTER CONNECT")

            logger.info("WebSocket connected.")

            print("WAITING FOR MESSAGE")

            async for message in websocket:

                print("HANDLE MESSAGE:", message)

                print("RAW MESSAGE:", message)

                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    logger.warning("Invalid message: %s", message)
                    continue

                print("PARSED:", data)

                logger.info("Received: %s", data)

                await self.handle_message(data)

    async def handle_message(self, message: dict) -> None:

        print("HANDLE MESSAGE:", message)

        action = message.get("action")

        print("ACTION:", action)

        if action not in {"BUY", "SELL", "CLOSE"}:
            logger.warning("Unknown message: %s", message)
            return

        print("EXECUTING TRADE")

        try:
            await self.executor.execute(message)
            logger.info("%s executed successfully.", action)

        except Exception:
            logger.exception("Trade execution failed.")