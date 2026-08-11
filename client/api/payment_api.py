import requests

from client.config import API_URL


class PaymentAPI:

    @staticmethod
    def submit_payment(
        token: str,
        file_path: str,
    ):

        try:
            with open(file_path, "rb") as payment_file:
                response = requests.post(
                    f"{API_URL}/subscriptions/payment",
                    headers={
                        "Authorization": f"Bearer {token}",
                    },
                    files={
                        "slip": payment_file,
                    },
                    timeout=30,
                )

        except (OSError, requests.RequestException) as e:
            print("PAYMENT REQUEST ERROR:", e)
            return None

        print("PAYMENT STATUS:", response.status_code)
        print("PAYMENT RESPONSE:", response.text)

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_payment_settings():

        try:
            response = requests.get(
                f"{API_URL}/subscriptions/payment-settings",
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_my_subscription(
        token: str,
    ):

        try:
            response = requests.get(
                f"{API_URL}/subscriptions/me",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException as e:
            print("SUBSCRIPTION STATUS ERROR:", e)
            return None

        if response.status_code == 200:
            return response.json()

        if response.status_code == 404:
            return {
                "status": "NOT_ACTIVE",
            }

        print(
            "SUBSCRIPTION STATUS:",
            response.status_code,
            response.text,
        )

        return None