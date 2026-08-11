import requests

from client.config import API_URL


class AuthAPI:

    @staticmethod
    def login_request(
        email: str,
        password: str,
    ):

        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={
                    "email": email,
                    "password": password,
                },
                timeout=10,
            )

        except requests.RequestException as e:
            print("LOGIN REQUEST ERROR:", e)

            return {
                "success": False,
                "message": f"Unable to connect to server: {e}",
            }

        print("LOGIN STATUS:", response.status_code)
        print("LOGIN RESPONSE:", response.text)

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