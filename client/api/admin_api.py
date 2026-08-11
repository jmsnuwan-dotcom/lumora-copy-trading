import requests

from client.config import API_URL


class AdminAPI:

    @staticmethod
    def get_payment_settings(token: str):

        try:
            response = requests.get(
                f"{API_URL}/admin/payment-settings",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def update_payment_settings(
        token: str,
        data: dict,
    ):

        try:
            response = requests.put(
                f"{API_URL}/admin/payment-settings",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json=data,
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_pending_payments(token: str):

        try:
            response = requests.get(
                f"{API_URL}/admin/payments/pending",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_payment_slip(
        token: str,
        subscription_id: int,
    ):
        try:
            response = requests.get(
                f"{API_URL}/admin/payments/{subscription_id}/slip",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException as e:
            print(
                "PAYMENT SLIP REQUEST ERROR:",
                e,
            )
            return None

        if response.status_code != 200:
            print(
                "PAYMENT SLIP ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.content

    @staticmethod
    def approve_payment(
        token: str,
        subscription_id: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/admin/payments/{subscription_id}/approve",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_clients(token: str):

        try:
            response = requests.get(
                f"{API_URL}/admin/clients",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def give_trial(
        token: str,
        subscription_id: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/admin/trial/{subscription_id}",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def activate_package(
        token: str,
        subscription_id: int,
    ):
        try:
            response = requests.post(
                f"{API_URL}/admin/package/{subscription_id}/activate",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def toggle_client_active(
        token: str,
        user_id: int,
    ):

        try:
            response = requests.put(
                f"{API_URL}/admin/clients/{user_id}/active",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            return None

        return response.json()

    @staticmethod
    def get_running_signals(
        token: str,
    ):

        try:
            response = requests.get(
                f"{API_URL}/signals/running",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            print(
                "RUNNING SIGNALS ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def get_signal_history(
        token: str,
    ):

        try:
            response = requests.get(
                f"{API_URL}/signals/history",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            print(
                "SIGNAL HISTORY ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def buy_trade(
        token: str,
        symbol: str,
        trade_id: str,
        magic_number: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/trades/buy",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "symbol": symbol,
                    "trade_id": trade_id,
                    "magic_number": magic_number,
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            print(
                "BUY ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def sell_trade(
        token: str,
        symbol: str,
        trade_id: str,
        magic_number: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/trades/sell",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "symbol": symbol,
                    "trade_id": trade_id,
                    "magic_number": magic_number,
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            print(
                "SELL ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()

    @staticmethod
    def close_trade(
        token: str,
        trade_id: str,
        magic_number: int,
    ):

        try:
            response = requests.post(
                f"{API_URL}/trades/close",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                json={
                    "trade_id": trade_id,
                    "magic_number": magic_number,
                },
                timeout=10,
            )

        except requests.RequestException:
            return None

        if response.status_code != 200:
            print(
                "CLOSE ERROR:",
                response.status_code,
                response.text,
            )
            return None

        return response.json()