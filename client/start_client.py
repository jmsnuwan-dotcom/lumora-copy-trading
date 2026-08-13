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

    print("START_CLIENT 1")

    print("MT5 LOGIN :", mt5_login)
    print("MT5 SERVER:", mt5_server)

    print("CONNECTING MT5")

    connected = MT5Client.connect(
        login=mt5_login,
        password=mt5_password,
        server=mt5_server,
    )

    if not connected:

        print("MT5 Connection Failed")
        print("Starting WebSocket without MT5...")

    print("START_CLIENT 2")
    print("MT5 Connected")

    HeartbeatAPI.send(
        token
    )

    print("START_CLIENT 3")

    asyncio.run(
        WebSocketClient(
            token=token,
            mt5_login=mt5_login,
            mt5_password=mt5_password,
            mt5_server=mt5_server,
        ).start()
    )

    print("START_CLIENT 4")