import time
import logging

from client.api.heartbeat_api import HeartbeatAPI
from client.mt5.trade_executor import TradeExecutor
from client.mt5.mt5_client import MT5Client
import MetaTrader5 as mt5


logger = logging.getLogger(__name__)


class PollingService:

    @staticmethod
    def run(token: str):

        logger.info("Polling service started.")

        while True:

            try:
                account = MT5Client.account_info()

                balance = None
                equity = None
                trade_condition = "NO TRADE"

                if account is not None:
                    balance = float(account.balance)
                    equity = float(account.equity)

                positions = mt5.positions_get()

                if positions:
                    has_buy = any(
                        position.type == mt5.ORDER_TYPE_BUY
                        for position in positions
                    )

                    has_sell = any(
                        position.type == mt5.ORDER_TYPE_SELL
                        for position in positions
                    )

                    if has_buy and has_sell:
                        trade_condition = "BUY + SELL"
                    elif has_buy:
                        trade_condition = "BUY"
                    elif has_sell:
                        trade_condition = "SELL"

                HeartbeatAPI.send(
                    token=token,
                    balance=balance,
                    equity=equity,
                    trade_condition=trade_condition,
                )


            except Exception as e:
                logger.exception(e)

            time.sleep(2)