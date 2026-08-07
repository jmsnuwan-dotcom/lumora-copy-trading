from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class WebSocketManager:
    """
    Manages connected client WebSockets.

    Key:
        user_id

    Value:
        One or more active WebSocket connections.
    """

    def __init__(self) -> None:
        self._connections: DefaultDict[int, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()

        async with self._lock:
            self._connections[user_id].add(websocket)

            print("=" * 50)
            print("CONNECTED USER :", user_id)
            print("ONLINE USERS   :", list(self._connections.keys()))
            print("COUNT          :", len(self._connections))
            print("=" * 50)

    async def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        async with self._lock:
            sockets = self._connections.get(user_id)

            if sockets is None:
                return

            sockets.discard(websocket)

            if not sockets:
                self._connections.pop(user_id, None)

            print("=" * 50)
            print("DISCONNECTED USER :", user_id)
            print("ONLINE USERS      :", list(self._connections.keys()))
            print("COUNT             :", len(self._connections))
            print("=" * 50)

    async def send(self, user_id: int, message: dict) -> None:
        async with self._lock:
            sockets = list(self._connections.get(user_id, set()))

        if not sockets:
            return

        dead_connections = []

        for websocket in sockets:
            try:
                await websocket.send_json(message)
            except Exception:
                dead_connections.append(websocket)

        if dead_connections:
            async with self._lock:
                current = self._connections.get(user_id)

                if current:
                    for websocket in dead_connections:
                        current.discard(websocket)

                    if not current:
                        self._connections.pop(user_id, None)

    async def is_online(self, user_id: int) -> bool:
        async with self._lock:

            print("=" * 50)
            print("CHECK USER :", user_id)
            print("ONLINE     :", list(self._connections.keys()))
            print("=" * 50)

            return user_id in self._connections

    async def online_count(self) -> int:
        async with self._lock:
            return len(self._connections)


websocket_manager = WebSocketManager()