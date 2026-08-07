import requests

from client.config import API_URL


class PackageAPI:

    @staticmethod
    def get_packages():

        response = requests.get(
            f"{API_URL}/packages",
            timeout=10,
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_plans(package_id: int):

        response = requests.get(
            f"{API_URL}/plans/{package_id}",
            timeout=10,
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_my_package(token: str):

        response = requests.get(
            f"{API_URL}/packages/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()