import requests

from client.config import API_URL


class TradeAPI:

    @staticmethod
    def buy(token: str, data: dict):

        response = requests.post(
            f"{API_URL}/signals",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "magic_number": data["magic_number"],
                "action": "BUY",
                "symbol": data["symbol"],
                "trade_count": data["trade_count"],
                "package": "BASIC",
                "entry_price": 0,
                "stop_loss": 0,
                "take_profit": 0,
                "comment": "Manual BUY",
            },
            timeout=10,
        )

        print(response.status_code)
        print(response.text)

        return response.status_code == 200

    @staticmethod
    def sell(token: str, data: dict):

        response = requests.post(
            f"{API_URL}/signals",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "magic_number": data["magic_number"],
                "action": "SELL",
                "symbol": data["symbol"],
                "trade_count": data["trade_count"],
                "package": "BASIC",
                "entry_price": 0,
                "stop_loss": 0,
                "take_profit": 0,
                "comment": "Manual SELL",
            },
            timeout=10,
        )

        print(response.status_code)
        print(response.text)

        return response.status_code == 200

    @staticmethod
    def close(token: str, magic_number: int):

        response = requests.post(
            f"{API_URL}/trades/close",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "magic_number": magic_number,
            },
            timeout=10,
        )

        print(response.status_code)
        print(response.text)

        return response.status_code == 200