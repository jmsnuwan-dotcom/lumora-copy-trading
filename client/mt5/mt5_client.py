import MetaTrader5 as mt5


class MT5Client:

    @staticmethod
    def connect(
        login: int,
        password: str,
        server: str,
    ) -> bool:

        if not mt5.initialize():
            print("MT5 initialize failed")
            return False

        authorized = mt5.login(
            login=login,
            password=password,
            server=server,
        )

        if not authorized:
            print("MT5 login failed")
            print(mt5.last_error())
            mt5.shutdown()
            return False

        account = mt5.account_info()

        if account is None:
            print("MT5 account info unavailable")
            mt5.shutdown()
            return False

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