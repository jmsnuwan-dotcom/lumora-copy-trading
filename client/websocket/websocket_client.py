import asyncio
import json
import logging
import ssl
from pathlib import Path

import certifi
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
    # LOCAL DIAGNOSTIC LOG
    # ==========================================================

    @staticmethod
    def _debug(message: str) -> None:

        try:

            log_dir = (
                Path.home()
                / "AppData"
                / "Local"
                / "Lumora"
                / "logs"
            )

            log_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            log_file = (
                log_dir
                / "websocket_client.log"
            )

            with log_file.open(
                "a",
                encoding="utf-8",
            ) as file:

                file.write(
                    message
                    + "\n"
                )

        except Exception:

            pass

    # ==========================================================
    # MAIN START
    # ==========================================================

    async def start(self) -> None:

        self._debug(
            "=" * 70
        )

        self._debug(
            "WEBSOCKET START"
        )

        print(
            "WEBSOCKET START"
        )

        market_data_task = asyncio.create_task(
            self._market_data_loop()
        )

        try:

            while True:

                try:

                    self._debug(
                        "CALLING _RUN"
                    )

                    print(
                        "CALLING _RUN"
                    )

                    await self._run()

                except httpx.HTTPStatusError as e:

                    self._debug(
                        f"WEBSOCKET HTTP STATUS ERROR: "
                        f"{e.response.status_code}"
                    )

                    if e.response.status_code in (
                        401,
                        403,
                    ):

                        self._debug(
                            "WEBSOCKET ACCESS DENIED"
                        )

                        print(
                            "WEBSOCKET ACCESS DENIED:",
                            e.response.text,
                        )

                        logger.warning(
                            "WebSocket stopped: "
                            "subscription/access denied."
                        )

                        return

                    self._debug(
                        f"HTTP ERROR: {repr(e)}"
                    )

                    print(
                        "WEBSOCKET HTTP ERROR:",
                        repr(e),
                    )

                    logger.exception(
                        "WebSocket HTTP error."
                    )

                    await asyncio.sleep(5)

                except Exception as e:

                    self._debug(
                        f"WEBSOCKET ERROR: {repr(e)}"
                    )

                    print(
                        "WEBSOCKET ERROR:",
                        repr(e),
                    )

                    logger.exception(
                        "WebSocket client stopped."
                    )

                    await asyncio.sleep(5)

        finally:

            self._debug(
                "WEBSOCKET START FINALLY"
            )

            market_data_task.cancel()

            try:

                await market_data_task

            except asyncio.CancelledError:

                pass

    # ==========================================================
    # MARKET DATA LOOP
    # ==========================================================

    async def _market_data_loop(self) -> None:

        self._debug(
            "MARKET DATA LOOP STARTED"
        )

        print(
            "MARKET DATA LOOP STARTED"
        )

        while True:

            try:

                MarketDataService.update_gold_price()

            except Exception as e:

                self._debug(
                    f"MARKET DATA ERROR: {repr(e)}"
                )

                logger.exception(
                    "Market data update failed."
                )

            await asyncio.sleep(1)

    # ==========================================================
    # WEBSOCKET CONNECTION
    # ==========================================================

    async def _run(self) -> None:

        self._debug(
            "ENTER _RUN"
        )

        print(
            "ENTER _RUN"
        )

        logger.info(
            "Registering MT5 connection..."
        )

        self._debug(
            "CONNECT START"
        )

        print(
            "CONNECT START"
        )

        self.connection = (
            await ConnectionService.connect(
                token=self.token,
                mt5_login=self.mt5_login,
                mt5_password=self.mt5_password,
                mt5_server=self.mt5_server,
            )
        )

        self._debug(
            "CONNECTION REGISTERED"
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

        self._debug(
            "WEBSOCKET URL CREATED"
        )

        self._debug(
            f"ACTUAL WS URL: {ws_url}"
        )

        print(
            "WS URL:",
            ws_url,
        )

        print(
            "BEFORE CONNECT"
        )

        self._debug(
            "BEFORE CONNECT"
        )

        ssl_context = ssl.create_default_context(
            cafile=certifi.where()
        )

        self._debug(
            f"SSL CA FILE: {certifi.where()}"
        )

        async with websockets.connect(
            ws_url,
            ssl=ssl_context,
            ping_interval=20,
            ping_timeout=20,
        ) as websocket:

            self._debug(
                "AFTER CONNECT"
            )

            print(
                "AFTER CONNECT"
            )

            logger.info(
                "WebSocket connected."
            )

            self._debug(
                "WEBSOCKET CONNECTED"
            )

            print(
                "WAITING FOR MESSAGE"
            )

            self._debug(
                "WAITING FOR MESSAGE"
            )

            async for message in websocket:

                self._debug(
                    "MESSAGE RECEIVED"
                )

                self._debug(
                    f"RAW MESSAGE: {message}"
                )

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

                except json.JSONDecodeError as e:

                    self._debug(
                        f"JSON DECODE ERROR: {repr(e)}"
                    )

                    logger.warning(
                        "Invalid message: %s",
                        message,
                    )

                    continue

                self._debug(
                    f"PARSED MESSAGE: {data}"
                )

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

        self._debug(
            "=" * 70
        )

        self._debug(
            "HANDLE MESSAGE"
        )

        self._debug(
            f"MESSAGE: {message}"
        )

        print(
            "HANDLE MESSAGE:",
            message,
        )

        action = message.get(
            "action"
        )

        self._debug(
            f"ACTION: {action}"
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

            self._debug(
                f"UNKNOWN ACTION: {action}"
            )

            logger.warning(
                "Unknown message: %s",
                message,
            )

            return

        self._debug(
            "VALID ACTION"
        )

        self._debug(
            "EXECUTING TRADE"
        )

        print(
            "EXECUTING TRADE"
        )

        try:

            await self.executor.execute(
                message
            )

            self._debug(
                f"EXECUTOR RETURNED: {action}"
            )

            logger.info(
                "%s executed successfully.",
                action,
            )

        except Exception as e:

            self._debug(
                f"TRADE EXECUTION EXCEPTION: {repr(e)}"
            )

            logger.exception(
                "Trade execution failed."
            )