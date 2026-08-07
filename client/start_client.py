import asyncio

from client.api.connection_api import ConnectionAPI
from client.api.heartbeat_api import HeartbeatAPI
from client.mt5.mt5_client import MT5Client
from client.mt5.symbol_loader import SymbolLoader
#from client.mt5.trade_monitor import TradeMonitor
from client.websocket.websocket_client import WebSocketClient


def start_client(token: str):

    print("START_CLIENT 1")

    if not MT5Client.connect():
        print("MT5 Connection Failed")
        return

    print("START_CLIENT 2")
    print("MT5 Connected")

    SymbolLoader.get_symbols()

    print("START_CLIENT 3")

    ConnectionAPI.save(token)

    print("START_CLIENT 4")

    HeartbeatAPI.send(token)

    print("START_CLIENT 5")

    asyncio.run(
        WebSocketClient(token).start()
    )