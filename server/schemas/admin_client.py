from datetime import datetime

from pydantic import BaseModel


class AdminClientResponse(BaseModel):
    id: int
    subscription_id: int

    full_name: str
    email: str
    phone_number: str | None = None

    status: str
    is_active: bool

    package: str | None = None
    plan: str | None = None
    payment_status: str | None = None

    is_trial: bool
    trial_ends_at: datetime | None = None

    start_date: datetime | None = None
    end_date: datetime | None = None

    # ==================================================
    # CONNECTION STATUS
    # ==================================================

    is_online: bool = False

    balance: float | None = None
    equity: float | None = None
    trade_condition: str | None = None