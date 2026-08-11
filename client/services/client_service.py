import threading

from client.start_client import start_client


class ClientService:

    @staticmethod
    def start(
        token: str,
        mt5_login: int,
        mt5_password: str,
        mt5_server: str,
    ):

        thread = threading.Thread(
            target=start_client,
            args=(
                token,
                mt5_login,
                mt5_password,
                mt5_server,
            ),
            daemon=True,
        )

        thread.start()