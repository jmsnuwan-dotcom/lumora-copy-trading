import threading

from client.start_client import start_client


class ClientService:

    @staticmethod
    def start(token: str):

        thread = threading.Thread(
            target=start_client,
            args=(token,),
            daemon=True,
        )

        thread.start()