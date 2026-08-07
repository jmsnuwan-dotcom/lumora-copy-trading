import asyncio
import logging

from client.mt5.mt5_client import MT5Client
from client.websocket.websocket_client import WebSocketClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main() -> None:

    if not MT5Client.connect():
        return

    client = WebSocketClient()
    await client.start()


if __name__ == "__main__":
    asyncio.run(main())