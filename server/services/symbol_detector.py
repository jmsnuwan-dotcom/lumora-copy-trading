import MetaTrader5 as mt5


class SymbolDetector:

    @staticmethod
    def get_symbols() -> list[str]:
        """
        Return all broker symbols.
        """

        symbols = mt5.symbols_get()

        if symbols is None:
            return []

        return [symbol.name for symbol in symbols]