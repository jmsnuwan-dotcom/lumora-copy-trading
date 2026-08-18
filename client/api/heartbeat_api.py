import requests

from client.config import API_URL


class HeartbeatAPI:

    @staticmethod
    def send(
        token: str,
        balance: float | None = None,
        equity: float | None = None,
        trade_condition: str | None = None,
    ):

        response = requests.post(
            f"{API_URL}/heartbeat",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "balance": balance,
                "equity": equity,
                "trade_condition": trade_condition,
            },
            timeout=10,
        )

        print(
            "HEARTBEAT RESPONSE:",
            response.status_code,
            response.text,
        )

        return response.status_code == 200