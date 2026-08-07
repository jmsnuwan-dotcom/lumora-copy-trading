import requests

from client.config import API_URL


class RegisterAPI:

    @staticmethod
    def register(
        full_name: str,
        email: str,
        phone: str,
        password: str,
        confirm_password: str,
        package_id: int,
        plan_id: int,
    ):

        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "phone_number": phone,
                "password": password,
                "confirm_password": confirm_password,
                "package_id": package_id,
                "plan_id": plan_id,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()