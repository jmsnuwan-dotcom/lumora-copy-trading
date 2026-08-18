import threading
import traceback
from pathlib import Path

from client.start_client import start_client
from client.services.polling_service import PollingService


LOG_DIR = (
    Path.home()
    / "AppData"
    / "Local"
    / "Lumora"
)

LOG_FILE = LOG_DIR / "client_start.log"


def _write_log(message: str):

    try:

        LOG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        with LOG_FILE.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                message + "\n"
            )

    except Exception:
        pass


def _run_client(
    token: str,
    mt5_login: int,
    mt5_password: str,
    mt5_server: str,
):

    _write_log(
        "CLIENT THREAD STARTED"
    )

    try:

        _write_log(
            "CALLING start_client()"
        )

        start_client(
            token=token,
            mt5_login=mt5_login,
            mt5_password=mt5_password,
            mt5_server=mt5_server,
        )

        _write_log(
            "start_client() RETURNED"
        )

    except Exception:

        _write_log(
            "CLIENT THREAD ERROR"
        )

        _write_log(
            traceback.format_exc()
        )


def _run_polling(
    token: str,
):

    _write_log(
        "POLLING THREAD STARTED"
    )

    try:

        PollingService.run(
            token
        )

    except Exception:

        _write_log(
            "POLLING THREAD ERROR"
        )

        _write_log(
            traceback.format_exc()
        )


class ClientService:

    @staticmethod
    def start(
        token: str,
        mt5_login: int,
        mt5_password: str,
        mt5_server: str,
    ):

        _write_log(
            "ClientService.start() CALLED"
        )

        # ==================================================
        # MT5 + WEBSOCKET THREAD
        # ==================================================

        client_thread = threading.Thread(
            target=_run_client,
            args=(
                token,
                mt5_login,
                mt5_password,
                mt5_server,
            ),
            daemon=True,
        )

        client_thread.start()

        _write_log(
            "CLIENT THREAD CREATED"
        )

        # ==================================================
        # HEARTBEAT + SIGNAL POLLING THREAD
        # ==================================================

        polling_thread = threading.Thread(
            target=_run_polling,
            args=(
                token,
            ),
            daemon=True,
        )

        polling_thread.start()

        _write_log(
            "POLLING THREAD CREATED"
        )