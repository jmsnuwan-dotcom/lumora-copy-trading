import MetaTrader5 as mt5


class SymbolLoader:

    @staticmethod
    def get_symbols() -> list[str]:

        symbols = mt5.symbols_get()

        if symbols is None:
            return []

        return [symbol.name for symbol in symbols]