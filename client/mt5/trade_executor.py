from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional, Tuple

import MetaTrader5 as mt5

from client.config import (
    DEVIATION,
    SL_DISTANCE,
    TP_DISTANCE,
)
from client.mt5.symbol_loader import SymbolLoader
from client.mt5.symbol_resolver import SymbolResolver
from client.storage.symbol_storage import SymbolStorage


logger = logging.getLogger(__name__)


class TradeExecutor:

    # ==========================================================
    # LOCAL DIAGNOSTIC LOG
    # ==========================================================

    @staticmethod
    def _debug(message: str) -> None:

        try:

            log_dir = (
                Path.home()
                / "AppData"
                / "Local"
                / "Lumora"
                / "logs"
            )

            log_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            log_file = (
                log_dir
                / "trade_executor.log"
            )

            with log_file.open(
                "a",
                encoding="utf-8",
            ) as file:

                file.write(
                    message
                    + "\n"
                )

        except Exception:

            pass

    # ==========================================================
    # EXECUTE
    # ==========================================================

    async def execute(
        self,
        message: dict,
    ) -> None:

        self._debug("=" * 70)
        self._debug("EXECUTOR RECEIVED")

        self._debug(
            json.dumps(
                message,
                default=str,
            )
        )

        print("=" * 60)
        print("EXECUTOR RECEIVED")
        print(message)
        print("=" * 60)

        action = message["action"]

        self._debug(
            f"ACTION: {action}"
        )

        if action == "BUY":

            await self._buy(
                message
            )

        elif action == "SELL":

            await self._sell(
                message
            )

        elif action == "CLOSE":

            await self._close(
                message
            )

        else:

            self._debug(
                f"UNKNOWN ACTION: {action}"
            )

    # ==========================================================
    # BUY
    # ==========================================================

    async def _buy(
        self,
        message: dict,
    ) -> None:

        trade_copies = int(
            message["trade_copies"]
        )

        self._debug(
            "BUY EXECUTE"
        )

        self._debug(
            f"TRADE COPIES: {trade_copies}"
        )

        print(
            "BUY EXECUTE"
        )

        for copy_number in range(
            trade_copies
        ):

            self._debug(
                f"BUY COPY START: "
                f"{copy_number + 1}/{trade_copies}"
            )

            self._open(
                volume=message["lot_size"],
                magic=message["magic_number"],
                order_type=mt5.ORDER_TYPE_BUY,
            )

            self._debug(
                f"BUY COPY END: "
                f"{copy_number + 1}/{trade_copies}"
            )

    # ==========================================================
    # SELL
    # ==========================================================

    async def _sell(
        self,
        message: dict,
    ) -> None:

        trade_copies = int(
            message["trade_copies"]
        )

        self._debug(
            "SELL EXECUTE"
        )

        self._debug(
            f"TRADE COPIES: {trade_copies}"
        )

        print(
            "SELL EXECUTE"
        )

        for copy_number in range(
            trade_copies
        ):

            self._debug(
                f"SELL COPY START: "
                f"{copy_number + 1}/{trade_copies}"
            )

            self._open(
                volume=message["lot_size"],
                magic=message["magic_number"],
                order_type=mt5.ORDER_TYPE_SELL,
            )

            self._debug(
                f"SELL COPY END: "
                f"{copy_number + 1}/{trade_copies}"
            )

    # ==========================================================
    # CLOSE
    # ==========================================================

    async def _close(
        self,
        message: dict,
    ) -> None:

        self._debug(
            "CLOSE EXECUTE"
        )

        magic = message["magic_number"]

        self._debug(
            f"CLOSE MAGIC: {magic}"
        )

        print(
            "CLOSE EXECUTE"
        )

        positions = mt5.positions_get()

        if positions is None:

            self._debug(
                "POSITIONS GET: NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            return

        self._debug(
            f"POSITIONS FOUND: {len(positions)}"
        )

        for position in positions:

            if position.magic != magic:
                continue

            self._debug(
                f"CLOSING POSITION: {position.ticket}"
            )

            self._close_position(
                position
            )

    # ==========================================================
    # SYMBOL
    # ==========================================================

    def _get_broker_symbol(
        self,
    ) -> Optional[str]:

        selected_symbol = (
            SymbolStorage.get_gold_symbol()
        )

        self._debug(
            f"SELECTED GOLD SYMBOL: "
            f"{selected_symbol}"
        )

        print(
            "SELECTED GOLD SYMBOL :",
            selected_symbol,
        )

        if not selected_symbol:

            self._debug(
                "NO GOLD SYMBOL SELECTED"
            )

            print(
                "NO GOLD SYMBOL SELECTED"
            )

            return None

        broker_symbols = (
            SymbolLoader.get_symbols()
        )

        self._debug(
            f"BROKER SYMBOL COUNT: "
            f"{len(broker_symbols) if broker_symbols else 0}"
        )

        if not broker_symbols:

            self._debug(
                "NO BROKER SYMBOLS FOUND"
            )

            print(
                "NO BROKER SYMBOLS FOUND"
            )

            return None

        broker_symbol = (
            SymbolResolver.resolve(
                selected_symbol,
                broker_symbols,
            )
        )

        self._debug(
            f"BROKER SYMBOL: {broker_symbol}"
        )

        print(
            "BROKER SYMBOL :",
            broker_symbol,
        )

        return broker_symbol

    # ==========================================================
    # FILLING MODE
    # ==========================================================

    def _get_filling_mode(
        self,
        symbol_info,
    ) -> Optional[int]:

        filling_flags = int(
            getattr(
                symbol_info,
                "filling_mode",
                0,
            )
            or 0
        )

        execution_mode = int(
            getattr(
                symbol_info,
                "trade_exemode",
                mt5.SYMBOL_TRADE_EXECUTION_INSTANT,
            )
        )

        self._debug(
            f"FILLING FLAGS: {filling_flags}"
        )

        self._debug(
            f"TRADE EXECUTION MODE: {execution_mode}"
        )

        print(
            "FILLING FLAGS :",
            filling_flags,
        )

        print(
            "TRADE EXECUTION MODE :",
            execution_mode,
        )

        # ======================================================
        # FOK
        # ======================================================

        if filling_flags & 1:
            self._debug(
                "SELECTED FILLING MODE: FOK"
            )

            print(
                "SELECTED FILLING MODE : FOK"
            )

            return mt5.ORDER_FILLING_FOK

        # ======================================================
        # IOC
        # ======================================================

        if filling_flags & 2:
            self._debug(
                "SELECTED FILLING MODE: IOC"
            )

            print(
                "SELECTED FILLING MODE : IOC"
            )

            return mt5.ORDER_FILLING_IOC

        # ======================================================
        # RETURN
        # ======================================================

        if (
            execution_mode
            != mt5.SYMBOL_TRADE_EXECUTION_MARKET
        ):
            self._debug(
                "SELECTED FILLING MODE: RETURN"
            )

            print(
                "SELECTED FILLING MODE : RETURN"
            )

            return mt5.ORDER_FILLING_RETURN

        # ======================================================
        # NO VALID MODE
        # ======================================================

        self._debug(
            "NO SUPPORTED FILLING MODE FOUND"
        )

        print(
            "NO SUPPORTED FILLING MODE FOUND"
        )

        return None
    # ==========================================================
    # OPEN
    # ==========================================================

    def _open(
        self,
        volume: float,
        magic: int,
        order_type: int,
    ) -> None:

        self._debug("=" * 70)

        self._debug(
            "OPEN START"
        )

        self._debug(
            f"LOT: {volume}"
        )

        self._debug(
            f"MAGIC: {magic}"
        )

        self._debug(
            f"ORDER TYPE: {order_type}"
        )

        print("=" * 60)
        print("OPEN START")
        print("LOT    :", volume)
        print("MAGIC  :", magic)
        print("=" * 60)

        broker_symbol = (
            self._get_broker_symbol()
        )

        if broker_symbol is None:

            self._debug(
                "BROKER GOLD SYMBOL NOT FOUND"
            )

            print(
                "BROKER GOLD SYMBOL NOT FOUND"
            )

            return

        self._debug(
            f"SYMBOL SELECT: {broker_symbol}"
        )

        if not mt5.symbol_select(
            broker_symbol,
            True,
        ):

            self._debug(
                f"SYMBOL SELECT FAILED: "
                f"{broker_symbol}"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

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

        self._debug(
            f"SYMBOL INFO: {symbol_info}"
        )

        self._debug(
            f"TICK: {tick}"
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

            self._debug(
                "SYMBOL INFO NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "SYMBOL INFO NONE"
            )

            return

        if tick is None:

            self._debug(
                "TICK NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "TICK NONE"
            )

            return

        # ------------------------------------------------------
        # DYNAMIC FILLING MODE
        # ------------------------------------------------------

        filling_mode = (
            self._get_filling_mode(
                symbol_info
            )
        )

        if filling_mode is None:

            self._debug(
                "OPEN ABORTED: "
                "NO SUPPORTED FILLING MODE"
            )

            print(
                "OPEN ABORTED: "
                "NO SUPPORTED FILLING MODE"
            )

            return

        # ------------------------------------------------------
        # PRICE
        # ------------------------------------------------------

        price = (
            tick.ask
            if order_type
            == mt5.ORDER_TYPE_BUY
            else tick.bid
        )

        # ------------------------------------------------------
        # SL / TP
        # ------------------------------------------------------

        sl, tp = self._calculate_sl_tp(
            price,
            order_type,
            symbol_info.point,
        )

        # ------------------------------------------------------
        # ORDER REQUEST
        # ------------------------------------------------------

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
            "type_filling": filling_mode,
        }

        self._debug(
            "ORDER REQUEST"
        )

        self._debug(
            json.dumps(
                request,
                default=str,
            )
        )

        print(
            "ORDER REQUEST"
        )

        print(
            request
        )

        # ------------------------------------------------------
        # ORDER CHECK
        # ------------------------------------------------------

        check = mt5.order_check(
            request
        )

        self._debug(
            f"ORDER CHECK: {check}"
        )

        print(
            "ORDER CHECK :",
            check,
        )

        if check is None:

            self._debug(
                "ORDER CHECK RETURNED NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "ORDER CHECK RETURNED NONE"
            )

        else:

            self._debug(
                f"ORDER CHECK RETCODE: "
                f"{check.retcode}"
            )

            self._debug(
                f"ORDER CHECK COMMENT: "
                f"{check.comment}"
            )

            print(
                "ORDER CHECK RETCODE :",
                check.retcode,
            )

            print(
                "ORDER CHECK COMMENT :",
                check.comment,
            )

        # ------------------------------------------------------
        # SEND
        # ------------------------------------------------------

        result = mt5.order_send(
            request
        )

        self._debug(
            f"ORDER RESULT: {result}"
        )

        print(
            "ORDER RESULT :",
            result,
        )

        if result is None:

            self._debug(
                "ORDER SEND RETURNED NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "ORDER SEND RETURNED NONE"
            )

            print(
                mt5.last_error()
            )

            return

        self._debug(
            f"RETCODE: {result.retcode}"
        )

        self._debug(
            f"COMMENT: {result.comment}"
        )

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

            self._debug(
                "ORDER FAILED"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "ORDER FAILED"
            )

            return

        self._debug(
            f"ORDER SUCCESS: {result.order}"
        )

        print(
            "ORDER SUCCESS :",
            result.order,
        )

        positions = mt5.positions_get(
            symbol=broker_symbol
        )

        self._debug(
            f"POSITIONS AFTER ORDER: "
            f"{len(positions) if positions is not None else 'NONE'}"
        )

        print("=" * 60)
        print(
            "POSITIONS AFTER ORDER"
        )

        if positions is None:

            self._debug(
                f"POSITIONS RESULT NONE - "
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "POSITIONS RESULT : NONE"
            )

            print(
                "MT5 LAST ERROR :",
                mt5.last_error(),
            )

        else:

            print(
                "POSITION COUNT :",
                len(positions),
            )

            for position in positions:

                self._debug(
                    f"POSITION: "
                    f"TICKET={position.ticket} "
                    f"SYMBOL={position.symbol} "
                    f"TYPE={position.type} "
                    f"VOLUME={position.volume} "
                    f"MAGIC={position.magic}"
                )

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

    # ==========================================================
    # SL / TP
    # ==========================================================

    def _calculate_sl_tp(
        self,
        price: float,
        order_type: int,
        point: float,
    ) -> Tuple[float, float]:

        if order_type == mt5.ORDER_TYPE_BUY:

            sl = price - SL_DISTANCE
            tp = price + TP_DISTANCE

        else:

            sl = price + SL_DISTANCE
            tp = price - TP_DISTANCE

        return (
            round(sl, 2),
            round(tp, 2),
        )

    # ==========================================================
    # CLOSE POSITION
    # ==========================================================

    def _close_position(
        self,
        position,
    ) -> None:

        self._debug(
            f"CLOSE POSITION: {position.ticket}"
        )

        print("=" * 60)
        print("CLOSE POSITION")
        print("TICKET :", position.ticket)
        print("SYMBOL :", position.symbol)
        print("MAGIC  :", position.magic)
        print("VOLUME :", position.volume)
        print("=" * 60)

        tick = mt5.symbol_info_tick(
            position.symbol
        )

        symbol_info = mt5.symbol_info(
            position.symbol
        )

        if tick is None:

            self._debug(
                f"CLOSE TICK NONE: "
                f"{position.symbol}"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "NO TICK"
            )

            return

        if symbol_info is None:

            self._debug(
                f"CLOSE SYMBOL INFO NONE: "
                f"{position.symbol}"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "CLOSE SYMBOL INFO NONE"
            )

            return

        # ------------------------------------------------------
        # DYNAMIC FILLING MODE FOR CLOSE
        # ------------------------------------------------------

        filling_mode = (
            self._get_filling_mode(
                symbol_info
            )
        )

        if filling_mode is None:

            self._debug(
                "CLOSE ABORTED: "
                "NO SUPPORTED FILLING MODE"
            )

            print(
                "CLOSE ABORTED: "
                "NO SUPPORTED FILLING MODE"
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
            "type_filling": filling_mode,
        }

        self._debug(
            "CLOSE REQUEST"
        )

        self._debug(
            json.dumps(
                request,
                default=str,
            )
        )

        print(
            "CLOSE REQUEST"
        )

        print(
            request
        )

        # ------------------------------------------------------
        # CLOSE ORDER CHECK
        # ------------------------------------------------------

        check = mt5.order_check(
            request
        )

        self._debug(
            f"CLOSE ORDER CHECK: {check}"
        )

        print(
            "CLOSE ORDER CHECK :",
            check,
        )

        if check is not None:

            self._debug(
                f"CLOSE CHECK RETCODE: "
                f"{check.retcode}"
            )

            self._debug(
                f"CLOSE CHECK COMMENT: "
                f"{check.comment}"
            )

            print(
                "CLOSE CHECK RETCODE :",
                check.retcode,
            )

            print(
                "CLOSE CHECK COMMENT :",
                check.comment,
            )

        result = mt5.order_send(
            request
        )

        self._debug(
            f"CLOSE RESULT: {result}"
        )

        print(
            "CLOSE RESULT :",
            result,
        )

        if result is None:

            self._debug(
                "CLOSE ORDER SEND NONE"
            )

            self._debug(
                f"MT5 ERROR: {mt5.last_error()}"
            )

            print(
                "ORDER SEND NONE"
            )

            print(
                mt5.last_error()
            )

            return

        self._debug(
            f"CLOSE RETCODE: {result.retcode}"
        )

        self._debug(
            f"CLOSE COMMENT: {result.comment}"
        )

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

            self._debug(
                f"CLOSE SUCCESS: "
                f"{position.ticket}"
            )

            print(
                "CLOSE SUCCESS :",
                position.ticket,
            )

        else:

            self._debug(
                "CLOSE FAILED"
            )

            print(
                "CLOSE FAILED"
            )