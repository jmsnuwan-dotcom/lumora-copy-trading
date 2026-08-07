import requests

from client.config import API_URL


class AuthAPI:

    @staticmethod
    def login_request(
        email: str,
        password: str,
    ):

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password,
            },
            timeout=10,
        )

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
            }

        try:
            message = response.json()["detail"]
        except Exception:
            message = "Login failed."

        return {
            "success": False,
            "message": message,
        }