from pydantic import BaseModel


from typing import Optional
from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    user_id: Optional[int] = None
    mt5_login: str
    mt5_password: str
    mt5_server: str


class ConnectionResponse(BaseModel):
    id: int
    user_id: int
    mt5_login: str
    mt5_server: str
    status: str

    balance: Optional[float] = None
    equity: Optional[float] = None
    trade_condition: Optional[str] = None

    class Config:
        from_attributes = True

