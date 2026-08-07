import requests

from client.config import API_URL
from client.mt5.mt5_client import MT5Client


class ConnectionAPI:

    @staticmethod
    def save(token: str):

        account = MT5Client.account_info()

        response = requests.post(
            f"{API_URL}/connections",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
               # "user_id": 0,  # තාවකාලිකයි
                "mt5_login": str(account.login),
                "mt5_password": "",
                "mt5_server": account.server,
            },
            timeout=10,
        )

        return response.status_code == 200

    @staticmethod
    def get_my_connection(token: str):

        response = requests.get(
            f"{API_URL}/connections/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()