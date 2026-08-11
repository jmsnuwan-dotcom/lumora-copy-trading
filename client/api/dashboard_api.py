import requests

from client.config import API_URL


class DashboardAPI:

    @staticmethod
    def get_dashboard(token: str):

        response = requests.get(
            f"{API_URL}/dashboard",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        print("DASHBOARD STATUS:", response.status_code)
        print("DASHBOARD RESPONSE:", response.text)

        if response.status_code == 200:
            return response.json()

        if response.status_code in (401, 403, 404):
            raise PermissionError(
                response.json().get(
                    "detail",
                    "Subscription is not active.",
                )
            )

        return None