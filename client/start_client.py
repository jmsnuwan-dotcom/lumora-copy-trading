import asyncio

from client.api.heartbeat_api import HeartbeatAPI
from client.mt5.mt5_client import MT5Client
from client.websocket.websocket_client import WebSocketClient


def start_client(
    token: str,
    mt5_login: int,
    mt5_password: str,
    mt5_server: str,
):

    connected = MT5Client.connect(
        login=mt5_login,
        password=mt5_password,
        server=mt5_server,
    )

    if not connected:
        return

    HeartbeatAPI.send(
        token
    )

    asyncio.run(
        WebSocketClient(
            token=token,
            mt5_login=mt5_login,
            mt5_password=mt5_password,
            mt5_server=mt5_server,
        ).start()
    )