from pydantic import BaseModel


class TradeCloseRequest(BaseModel):
    magic_number: int