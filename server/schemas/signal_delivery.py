from pydantic import BaseModel


class SignalExecutedRequest(BaseModel):
    delivery_id: int
    mt5_ticket: int


class SignalClosedRequest(BaseModel):
    delivery_id: int