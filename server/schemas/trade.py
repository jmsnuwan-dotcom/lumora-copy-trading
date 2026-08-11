from pydantic import BaseModel, Field


class BuyTradeRequest(BaseModel):
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    trade_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class SellTradeRequest(BaseModel):
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    trade_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class CloseTradeRequest(BaseModel):
    trade_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    magic_number: int = Field(
        ...,
        gt=0,
    )