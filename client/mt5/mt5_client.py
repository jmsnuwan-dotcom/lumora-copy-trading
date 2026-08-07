import MetaTrader5 as mt5

from client.config import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
)


class MT5Client:

    @staticmethod
    def connect() -> bool:

        if not mt5.initialize():
            print("MT5 initialize failed")
            return False

        authorized = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER,
        )

        if not authorized:
            print("MT5 login failed")
            print(mt5.last_error())
            return False

        account = mt5.account_info()

        if account is not None:
            print("=" * 40)
            print("LOGIN :", account.login)
            print("NAME  :", account.name)
            print("SERVER:", account.server)
            print("=" * 40)

        return True

    @staticmethod
    def shutdown():
        mt5.shutdown()

    @staticmethod
    def account_info():
        return mt5.account_info()

    @staticmethod
    def symbols():
        return mt5.symbols_get()