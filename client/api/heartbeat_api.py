import requests

from client.config import API_URL


class HeartbeatAPI:

    @staticmethod
    def send(token: str):

        response = requests.post(
            f"{API_URL}/heartbeat",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10,
        )

        return response.status_code == 200