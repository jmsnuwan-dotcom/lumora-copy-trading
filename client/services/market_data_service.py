from typing import Optional

import MetaTrader5 as mt5

from client.storage.symbol_storage import SymbolStorage


class MarketDataService:

    _price: Optional[float] = None

    @classmethod
    def get_gold_symbol(cls) -> Optional[str]:

        symbol = SymbolStorage.get_gold_symbol()

        if not symbol:
            return None

        return symbol.strip()

    @classmethod
    def update_gold_price(cls) -> Optional[float]:

        try:

            symbol = cls.get_gold_symbol()

            if not symbol:
                cls._price = None
                return None

            if not mt5.symbol_select(
                symbol,
                True,
            ):
                cls._price = None
                return None

            tick = mt5.symbol_info_tick(
                symbol
            )

            if tick is None:
                cls._price = None
                return None

            price = float(tick.bid)

            if price <= 0:
                cls._price = None
                return None

            cls._price = price

            return price

        except Exception:

            cls._price = None
            return None

    @classmethod
    def get_gold_price(cls) -> Optional[float]:

        return cls._price