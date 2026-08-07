from datetime import UTC, datetime, timedelta


class OnlineClientRegistry:

    _clients: dict[int, datetime] = {}

    @classmethod
    def heartbeat(cls, user_id: int):
        cls._clients[user_id] = datetime.now(UTC)

    @classmethod
    def is_online(cls, user_id: int) -> bool:
        last_seen = cls._clients.get(user_id)

        if last_seen is None:
            return False

        return datetime.now(UTC) - last_seen < timedelta(seconds=30)

    @classmethod
    def remove(cls, user_id: int):
        cls._clients.pop(user_id, None)