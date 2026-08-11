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

        try:
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

        except requests.RequestException as e:
            print("REGISTER REQUEST ERROR:", e)
            return None

        if response.status_code != 200:
            print("REGISTER STATUS:", response.status_code)
            print("REGISTER RESPONSE:", response.text)
            return None

        return response.json()