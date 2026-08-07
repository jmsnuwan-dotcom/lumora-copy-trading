from dataclasses import dataclass


@dataclass
class Signal:
    id: int
    symbol: str
    signal_type: str
    entry: float
    stop_loss: float
    take_profit: float