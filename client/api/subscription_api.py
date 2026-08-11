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

    @staticmethod
    def create_subscription(
        token: str,
        package_id: int,
        plan_id: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/subscriptions",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "package_id": package_id,
                    "plan_id": plan_id,
                    "status": "PENDING",
                },
                timeout=10,
            )

        except requests.RequestException as e:
            print(
                "CREATE SUBSCRIPTION ERROR:",
                e,
            )
            return None

        if response.status_code != 200:
            print(
                "CREATE SUBSCRIPTION STATUS:",
                response.status_code,
            )
            print(
                "CREATE SUBSCRIPTION RESPONSE:",
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def create_subscription(
        token: str,
        package_id: int,
        plan_id: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/subscriptions",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "user_id": 0,
                    "package_id": package_id,
                    "plan_id": plan_id,
                    "approved_by": 0,
                    "status": "PENDING",
                },
                timeout=10,
            )

        except requests.RequestException as e:
            print(
                "CREATE SUBSCRIPTION ERROR:",
                e,
            )
            return None

        if response.status_code != 200:
            print(
                "CREATE SUBSCRIPTION STATUS:",
                response.status_code,
            )
            print(
                "CREATE SUBSCRIPTION RESPONSE:",
                response.text,
            )
            return None

        return response.json()