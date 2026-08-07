import time
import logging

from client.api.heartbeat_api import HeartbeatAPI
from client.api.signal_api import SignalAPI
from client.api.signal_delivery_api import SignalDeliveryAPI
from client.mt5.trade_executor import TradeExecutor
from client.api.package_api import PackageAPI


logger = logging.getLogger(__name__)


class PollingService:

    @staticmethod
    def run(token: str):

        logger.info("Polling service started.")

        last_package_sync = 0

        while True:

            try:
                HeartbeatAPI.send(token)

                if time.time() - last_package_sync >= 60:
                    PackageAPI.sync(token)
                    last_package_sync = time.time()

                signals = SignalAPI.get_received_signals(token)
                
                if signals is None:
                    time.sleep(2)
                    continue

                for signal in signals:

                    logger.info(
                        f"Executing Signal: {signal['delivery_id']}"
                    )

                    result = TradeExecutor.execute(signal)

                    if result is None:
                        logger.warning("Trade execution failed.")
                        continue

                    SignalDeliveryAPI.mark_executed(
                        token=token,
                        delivery_id=signal["delivery_id"],
                        mt5_ticket=result.order,
                    )

                    logger.info(
                        f"Trade Executed: {result.order}"
                    )

            except Exception as e:
                logger.exception(e)

            time.sleep(2)