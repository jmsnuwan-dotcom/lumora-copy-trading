import json
from pathlib import Path


class TradeStore:

    def __init__(self):
        self.file = Path("client/storage/trades.json")

        if not self.file.exists():
            self.file.write_text("{}")

    def load(self) -> dict:
        return json.loads(self.file.read_text())

    def save(
        self,
        trade_id: str,
        ticket: int,
    ):

        data = self.load()

        if trade_id not in data:
            data[trade_id] = []

        data[trade_id].append(ticket)

        self.file.write_text(
            json.dumps(data, indent=4),
        )

    def get(
        self,
        trade_id: str,
    ) -> list[int]:

        data = self.load()

        return data.get(trade_id, [])

    def remove(
        self,
        trade_id: str,
    ):

        data = self.load()

        if trade_id in data:
            del data[trade_id]

        self.file.write_text(
            json.dumps(data, indent=4),
        )