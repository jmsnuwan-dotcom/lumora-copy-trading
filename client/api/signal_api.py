import requests

from client.config import API_URL


class SignalAPI:

    @staticmethod
    def get_received_signals(token: str):

        response = requests.get(
            f"{API_URL}/signals/received",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()

        print(response.text)
        return []