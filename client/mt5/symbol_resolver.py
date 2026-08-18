from typing import List, Optional


class SymbolResolver:

    @staticmethod
    def resolve(
        canonical_symbol: str,
        broker_symbols: List[str],
    ) -> Optional[str]:

        canonical = canonical_symbol.upper()

        for symbol in broker_symbols:
            if symbol.upper() == canonical:
                return symbol

        for symbol in broker_symbols:
            if canonical in symbol.upper():
                return symbol

        clean = canonical.replace("/", "").replace(".", "")

        for symbol in broker_symbols:

            current = (
                symbol.upper()
                .replace("/", "")
                .replace(".", "")
            )

            if clean in current:
                return symbol

        return None