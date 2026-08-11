import requests

from client.config import API_URL


class PackageAPI:

    @staticmethod
    def get_packages():

        response = requests.get(
            f"{API_URL}/packages",
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def create_package(
        token: str,
        name: str,
        lot_size: float,
        trades_per_signal: int,
    ):

        response = requests.post(
            f"{API_URL}/packages",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": name,
                "lot_size": lot_size,
                "trades_per_signal": trades_per_signal,
            },
            timeout=10,
        )

        if response.status_code != 200:
            print(
                "CREATE PACKAGE ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def update_package(
        token: str,
        package_id: int,
        name: str,
        lot_size: float,
        trades_per_signal: int,
    ):

        response = requests.put(
            f"{API_URL}/packages/{package_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": name,
                "lot_size": lot_size,
                "trades_per_signal": trades_per_signal,
            },
            timeout=10,
        )

        if response.status_code != 200:
            print(
                "UPDATE PACKAGE ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def disable_package(
        token: str,
        package_id: int,
    ):

        response = requests.delete(
            f"{API_URL}/packages/{package_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )

        if response.status_code != 200:
            print(
                "DISABLE PACKAGE ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def get_plans(
        package_id: int,
    ):

        response = requests.get(
            f"{API_URL}/plans/{package_id}",
            timeout=10,
        )

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_my_package(
        token: str,
    ):

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