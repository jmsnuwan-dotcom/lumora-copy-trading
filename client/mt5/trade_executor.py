from __future__ import annotations

import logging

import MetaTrader5 as mt5

from client.config import (
    DEVIATION,
    SL_POINTS,
    RR,
)
from client.mt5.symbol_loader import SymbolLoader
from client.mt5.symbol_resolver import SymbolResolver
from client.storage.symbol_storage import SymbolStorage

logger = logging.getLogger(__name__)


class TradeExecutor:

    async def execute(self, message: dict) -> None:

        print("=" * 60)
        print("EXECUTOR RECEIVED")
        print(message)
        print("=" * 60)

        action = message["action"]

        if action == "BUY":
            await self._buy(message)

        elif action == "SELL":
            await self._sell(message)

        elif action == "CLOSE":
            await self._close(message)

    async def _buy(self, message: dict) -> None:

        print("BUY EXECUTE")

        for _ in range(message["trade_copies"]):

            self._open(
                volume=message["lot_size"],
                magic=message["magic_number"],
                order_type=mt5.ORDER_TYPE_BUY,
            )

    async def _sell(self, message: dict) -> None:

        print("SELL EXECUTE")

        for _ in range(message["trade_copies"]):

            self._open(
                volume=message["lot_size"],
                magic=message["magic_number"],
                order_type=mt5.ORDER_TYPE_SELL,
            )

    async def _close(self, message: dict) -> None:

        print("CLOSE EXECUTE")

        magic = message["magic_number"]

        positions = mt5.positions_get()

        if positions is None:
            return

        for position in positions:

            if position.magic != magic:
                continue

            self._close_position(position)

    def _get_broker_symbol(self) -> str | None:

        selected_symbol = (
            SymbolStorage.get_gold_symbol()
        )

        print(
            "SELECTED GOLD SYMBOL :",
            selected_symbol,
        )

        if not selected_symbol:
            print(
                "NO GOLD SYMBOL SELECTED"
            )
            return None

        broker_symbols = (
            SymbolLoader.get_symbols()
        )

        if not broker_symbols:
            print(
                "NO BROKER SYMBOLS FOUND"
            )
            return None

        broker_symbol = SymbolResolver.resolve(
            selected_symbol,
            broker_symbols,
        )

        print(
            "BROKER SYMBOL :",
            broker_symbol,
        )

        return broker_symbol

    def _open(
        self,
        volume: float,
        magic: int,
        order_type: int,
    ) -> None:

        print("=" * 60)
        print("OPEN START")
        print("LOT    :", volume)
        print("MAGIC  :", magic)
        print("=" * 60)

        broker_symbol = (
            self._get_broker_symbol()
        )

        if broker_symbol is None:

            print(
                "BROKER GOLD SYMBOL NOT FOUND"
            )

            return

        if not mt5.symbol_select(
            broker_symbol,
            True,
        ):

            print(
                "SYMBOL SELECT FAILED :",
                broker_symbol,
            )

            return

        tick = mt5.symbol_info_tick(
            broker_symbol
        )

        symbol_info = mt5.symbol_info(
            broker_symbol
        )

        print(
            "SYMBOL INFO :",
            symbol_info,
        )

        print(
            "TICK :",
            tick,
        )

        if symbol_info is None:

            print(
                "SYMBOL INFO NONE"
            )

            return

        if tick is None:

            print(
                "TICK NONE"
            )

            return

        price = (
            tick.ask
            if order_type == mt5.ORDER_TYPE_BUY
            else tick.bid
        )

        sl, tp = self._calculate_sl_tp(
            price,
            order_type,
            symbol_info.point,
        )

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": broker_symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": DEVIATION,
            "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        print("ORDER REQUEST")
        print(request)

        result = mt5.order_send(request)

        print(
            "ORDER RESULT :",
            result,
        )

        if result is None:

            print(
                "ORDER SEND RETURNED NONE"
            )

            print(
                mt5.last_error()
            )

            return

        print(
            "RETCODE :",
            result.retcode,
        )

        print(
            "COMMENT :",
            result.comment,
        )

        if (
            result.retcode
            != mt5.TRADE_RETCODE_DONE
        ):

            print(
                "ORDER FAILED"
            )

            return

        print(
            "ORDER SUCCESS :",
            result.order,
        )

        positions = mt5.positions_get(
            symbol=broker_symbol
        )

        print("=" * 60)
        print("POSITIONS AFTER ORDER")

        if positions is None:
            print(
                "POSITIONS RESULT : NONE"
            )
            print(
                "MT5 LAST ERROR :",
                mt5.last_error()
            )

        else:
            print(
                "POSITION COUNT :",
                len(positions)
            )

            for position in positions:
                print(
                    "TICKET :",
                    position.ticket,
                    "SYMBOL :",
                    position.symbol,
                    "TYPE :",
                    position.type,
                    "VOLUME :",
                    position.volume,
                    "MAGIC :",
                    position.magic,
                )

        print("=" * 60)

    def _calculate_sl_tp(
        self,
        price: float,
        order_type: int,
        point: float,
    ) -> tuple[float, float]:

        tp_points = SL_POINTS * RR

        if order_type == mt5.ORDER_TYPE_BUY:

            sl = price - (
                SL_POINTS * point
            )

            tp = price + (
                tp_points * point
            )

        else:

            sl = price + (
                SL_POINTS * point
            )

            tp = price - (
                tp_points * point
            )

        return (
            round(sl, 2),
            round(tp, 2),
        )

    def _close_position(
        self,
        position,
    ) -> None:

        print("=" * 60)
        print("CLOSE POSITION")
        print(
            "TICKET :",
            position.ticket,
        )
        print(
            "SYMBOL :",
            position.symbol,
        )
        print(
            "MAGIC  :",
            position.magic,
        )
        print(
            "VOLUME :",
            position.volume,
        )
        print("=" * 60)

        tick = mt5.symbol_info_tick(
            position.symbol
        )

        if tick is None:

            print(
                "NO TICK"
            )

            return

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": (
                mt5.ORDER_TYPE_SELL
                if position.type
                == mt5.ORDER_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            ),
            "price": (
                tick.bid
                if position.type
                == mt5.ORDER_TYPE_BUY
                else tick.ask
            ),
            "deviation": DEVIATION,
            "magic": position.magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        print("CLOSE REQUEST")
        print(request)

        result = mt5.order_send(request)

        print(
            "CLOSE RESULT :",
            result,
        )

        if result is None:

            print(
                "ORDER SEND NONE"
            )

            print(
                mt5.last_error()
            )

            return

        print(
            "RETCODE :",
            result.retcode,
        )

        print(
            "COMMENT :",
            result.comment,
        )

        if (
            result.retcode
            == mt5.TRADE_RETCODE_DONE
        ):

            print(
                "CLOSE SUCCESS :",
                position.ticket,
            )

        else:

            print(
                "CLOSE FAILED"
            )