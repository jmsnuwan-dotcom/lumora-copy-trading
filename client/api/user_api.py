import requests

from client.config import API_URL


class UserAPI:

    @staticmethod
    def me(token: str):

        response = requests.get(
            f"{API_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def toggle_signals(token: str):

        response = requests.put(
            f"{API_URL}/users/signals",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()