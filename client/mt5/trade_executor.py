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
                symbol=message["symbol"],
                volume=message["lot_size"],
                magic=message["magic_number"],
                order_type=mt5.ORDER_TYPE_BUY,
            )

    async def _sell(self, message: dict) -> None:

        print("SELL EXECUTE")

        for _ in range(message["trade_copies"]):
            self._open(
                symbol=message["symbol"],
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

    def _open(
        self,
        symbol: str,
        volume: float,
        magic: int,
        order_type: int,
    ) -> None:

        print("=" * 60)
        print("OPEN START")
        print("SYMBOL :", symbol)
        print("LOT    :", volume)
        print("MAGIC  :", magic)
        print("=" * 60)

        broker_symbols = SymbolLoader.get_symbols()

        broker_symbol = SymbolResolver.resolve(
            symbol,
            broker_symbols,
        )

        print("BROKER SYMBOL :", broker_symbol)

        if broker_symbol is None:
            print("BROKER SYMBOL NOT FOUND")
            return

        tick = mt5.symbol_info_tick(broker_symbol)
        symbol_info = mt5.symbol_info(broker_symbol)

        print("SYMBOL INFO :", symbol_info)
        print("TICK :", tick)

        if symbol_info is None:
            print("SYMBOL INFO NONE")
            return

        if tick is None:
            print("TICK NONE")
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

        print("ORDER RESULT :", result)

        if result is None:
            print("ORDER SEND RETURNED NONE")
            print(mt5.last_error())
            return

        print("RETCODE :", result.retcode)
        print("COMMENT :", result.comment)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("ORDER FAILED")
            return

        print("ORDER SUCCESS :", result.order)

    def _calculate_sl_tp(
        self,
        price: float,
        order_type: int,
        point: float,
    ) -> tuple[float, float]:

        tp_points = SL_POINTS * RR

        if order_type == mt5.ORDER_TYPE_BUY:
            sl = price - (SL_POINTS * point)
            tp = price + (tp_points * point)
        else:
            sl = price + (SL_POINTS * point)
            tp = price - (tp_points * point)

        return (
            round(sl, 2),
            round(tp, 2),
        )

    def _close_position(self, position) -> None:

        print("=" * 60)
        print("CLOSE POSITION")
        print("TICKET :", position.ticket)
        print("SYMBOL :", position.symbol)
        print("MAGIC  :", position.magic)
        print("VOLUME :", position.volume)
        print("=" * 60)

        tick = mt5.symbol_info_tick(position.symbol)

        if tick is None:
            print("NO TICK")
            return

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": (
                mt5.ORDER_TYPE_SELL
                if position.type == mt5.ORDER_TYPE_BUY
                else mt5.ORDER_TYPE_BUY
            ),
            "price": (
                tick.bid
                if position.type == mt5.ORDER_TYPE_BUY
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

        print("CLOSE RESULT :", result)

        if result is None:
            print("ORDER SEND NONE")
            print(mt5.last_error())
            return

        print("RETCODE :", result.retcode)
        print("COMMENT :", result.comment)

        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print("CLOSE SUCCESS :", position.ticket)
        else:
            print("CLOSE FAILED")