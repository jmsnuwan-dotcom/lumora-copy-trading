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

        if response.status_code != 200:
            return None

        data = response.json()
        
        return data