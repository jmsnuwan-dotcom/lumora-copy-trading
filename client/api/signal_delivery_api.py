import requests


class SignalDeliveryAPI:

    BASE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def mark_executed(
        token: str,
        delivery_id: int,
        mt5_ticket: int,
    ):

        response = requests.post(
            f"{SignalDeliveryAPI.BASE_URL}/signal-deliveries/executed",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "delivery_id": delivery_id,
                "mt5_ticket": mt5_ticket,
            },
            timeout=10,
        )

        return response.ok