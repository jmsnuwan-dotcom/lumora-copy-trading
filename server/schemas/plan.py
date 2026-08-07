from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PlanResponse(BaseModel):

    id: int
    public_id: str
    package_id: int
    name: str
    duration_days: int | None
    price: Decimal
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )