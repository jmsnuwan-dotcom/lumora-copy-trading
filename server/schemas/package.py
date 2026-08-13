from decimal import Decimal

from pydantic import BaseModel


class PackageCreate(BaseModel):
    name: str
    lot_size: Decimal
    trades_per_signal: int
    monthly_price: Decimal
    lifetime_price: Decimal


class PackageResponse(BaseModel):
    id: int
    name: str
    lot_size: Decimal
    trades_per_signal: int
    is_active: bool

    class Config:
        from_attributes = True