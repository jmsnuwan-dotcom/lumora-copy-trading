class SymbolMapper:

    @staticmethod
    def find_best_match(
        master_symbol: str,
        broker_symbols: list[str],
    ) -> str | None:

        master = master_symbol.upper()

        # Exact match
        for symbol in broker_symbols:
            if symbol.upper() == master:
                return symbol

        # Contains match
        for symbol in broker_symbols:
            if master in symbol.upper():
                return symbol

        return None