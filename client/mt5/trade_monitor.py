import threading
import time
import MetaTrader5 as mt5

from client.database.open_trade_cache import OpenTradeCache
from client.api.trade_api import TradeAPI


class TradeMonitor:

    @staticmethod
    def start(token):

        thread = threading.Thread(
            target=TradeMonitor.run,
            args=(token,),
            daemon=True,
        )

        thread.start()

    @staticmethod
    def run(token):

        print("Trade Monitor Started")

        while True:

            try:

                positions = mt5.positions_get()

                if positions is None:
                    time.sleep(1)
                    continue

                current = set()

                for position in positions:

                    if position.magic == 100001:
                        continue

                    current.add(position.ticket)
                    OpenTradeCache.magic_numbers[position.ticket] = position.magic

                    print(
                        f"Trade : "
                        f"{position.ticket} "
                        f"{position.symbol} "
                        f"{position.type}"
                    )

                new_trades = current - OpenTradeCache.previous

                for position in positions:

                    if position.magic == 100001:
                        continue

                    if position.ticket not in new_trades:
                        continue

                    print(f"NEW TRADE : {position.ticket}")

                    data = {
                        "symbol": position.symbol,
                        "action": (
                            "BUY"
                            if position.type == mt5.ORDER_TYPE_BUY
                            else "SELL"
                        ),
                        "trade_count": 1,
                        "magic_number": position.magic,
                    }

                    if position.type == mt5.ORDER_TYPE_BUY:
                        print("BUY Signal Sent To Server")
                        TradeAPI.buy(token, data)
                    else:
                        print("SELL Signal Sent To Server")
                        TradeAPI.sell(token, data)

                closed_trades = OpenTradeCache.previous - current

                print("PREVIOUS :", OpenTradeCache.previous)
                print("CURRENT  :", current)

                for ticket in closed_trades:

                    magic = OpenTradeCache.magic_numbers.get(ticket)

                    if magic is None:
                        continue

                    print(f"CLOSED TRADE : {ticket}")

                    print("========== CLOSE DETECTED ==========")
                    print(f"Ticket : {ticket}")
                    print(f"Magic  : {magic}")

                    TradeAPI.close(
                        token,
                        magic,
                    )

                    del OpenTradeCache.magic_numbers[ticket]

                OpenTradeCache.tickets = current
                OpenTradeCache.previous = current

            except Exception as e:
                print("Trade Monitor Error:", e)

            time.sleep(1)