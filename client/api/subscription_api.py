import requests

from client.config import API_URL


class SubscriptionAPI:

    @staticmethod
    def get_my_subscription(token: str):

        response = requests.get(
            f"{API_URL}/subscriptions/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()