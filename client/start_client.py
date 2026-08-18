import asyncio
import os
import traceback
from pathlib import Path

from client.api.heartbeat_api import HeartbeatAPI
from client.mt5.mt5_client import MT5Client
from client.websocket.websocket_client import WebSocketClient


LOG_FILE = (
    Path(os.getenv("LOCALAPPDATA", Path.home()))
    / "Lumora"
    / "client_start.log"
)


def _log(message: str) -> None:

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with LOG_FILE.open(
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            f"{message}\n"
        )


def start_client(
    token: str,
    mt5_login: int,
    mt5_password: str,
    mt5_server: str,
):

    _log("=" * 60)
    _log("START_CLIENT ENTERED")
    _log(
        f"MT5 LOGIN: {mt5_login}"
    )
    _log(
        f"MT5 SERVER: {mt5_server}"
    )

    try:

        # ==================================================
        # STEP 1 — MT5 CONNECT
        # ==================================================

        _log(
            "STEP 1: MT5 CONNECT START"
        )

        connected = MT5Client.connect(
            login=mt5_login,
            password=mt5_password,
            server=mt5_server,
        )

        _log(
            f"STEP 1: MT5 CONNECT RESULT = {connected}"
        )

        if not connected:

            _log(
                "STOP: MT5 CONNECTION FAILED"
            )

            return

        # ==================================================
        # STEP 2 — INITIAL HEARTBEAT
        # ==================================================

        _log(
            "STEP 2: HEARTBEAT START"
        )

        account = MT5Client.account_info()

        balance = None
        equity = None

        if account is not None:

            balance = float(
                account.balance
            )

            equity = float(
                account.equity
            )

        HeartbeatAPI.send(
            token=token,
            balance=balance,
            equity=equity,
        )

        _log(
            "STEP 2: HEARTBEAT COMPLETE"
        )

        # ==================================================
        # STEP 3 — WEBSOCKET
        # ==================================================

        _log(
            "STEP 3: WEBSOCKET CLIENT CREATE"
        )

        websocket_client = WebSocketClient(
            token=token,
            mt5_login=mt5_login,
            mt5_password=mt5_password,
            mt5_server=mt5_server,
        )

        _log(
            "STEP 3: WEBSOCKET CLIENT CREATED"
        )

        _log(
            "STEP 4: ASYNCIO RUN START"
        )

        _log(
            f"WEBSOCKET OBJECT: "
            f"{websocket_client!r}"
        )

        _log(
            f"WEBSOCKET START METHOD: "
            f"{websocket_client.start!r}"
        )

        _log(
            f"START METHOD TYPE: "
            f"{type(websocket_client.start)}"
        )

        asyncio.run(
            websocket_client.start()
        )

        _log(
            "STEP 4: ASYNCIO RUN ENDED"
        )

    except Exception as e:

        _log(
            "!!! START_CLIENT EXCEPTION !!!"
        )

        _log(
            f"EXCEPTION TYPE: "
            f"{type(e).__name__}"
        )

        _log(
            f"EXCEPTION: "
            f"{repr(e)}"
        )

        _log(
            traceback.format_exc()
        )

        _log(
            "!!! START_CLIENT STOPPED !!!"
        )