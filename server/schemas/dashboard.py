from datetime import datetime

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    full_name: str
    email: str

    package: str
    plan: str

    lot_size: float

    status: str

    expire_date: datetime | None

    connection_status: str | None = None

    balance: float | None = None

    equity: float | None = None

    open_trades: int | None = None

    remaining_days: int | None = None

    signals_enabled: bool

    class Config:
        from_attributes = True