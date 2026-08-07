import httpx

from client.config import API_URL


class ConnectionService:

    CONNECTION_URL = f"{API_URL}/connections"

    @classmethod
    async def connect(
        cls,
        token: str,
        mt5_login: int,
        mt5_password: str,
        mt5_server: str,
    ) -> dict:

        print("CONNECT REQUEST")

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.post(
                cls.CONNECTION_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "mt5_login": str(mt5_login),
                    "mt5_password": mt5_password,
                    "mt5_server": mt5_server,
                },
            )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        response.raise_for_status()

        print("RETURNING JSON")

        return response.json()