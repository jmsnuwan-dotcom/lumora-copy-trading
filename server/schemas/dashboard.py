from datetime import datetime

from pydantic import BaseModel


class DashboardResponse(BaseModel):
    full_name: str
    email: str

    package: str
    plan: str
    lot_size: float

    status: str
    is_active: bool

    start_date: datetime | None
    expire_date: datetime | None

    is_trial: bool
    trial_ends_at: datetime | None

    connection_status: str | None = None
    mt5_login: str | None = None
    mt5_server: str | None = None
    last_seen: datetime | None = None
    client_version: str | None = None

    balance: float | None = None
    equity: float | None = None
    open_trades: int | None = None

    remaining_days: int | None = None

    signals_enabled: bool

    class Config:
        from_attributes = True