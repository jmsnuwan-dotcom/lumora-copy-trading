from datetime import datetime

from pydantic import BaseModel
from server.schemas.package import PackageResponse
from server.schemas.plan import PlanResponse

class SubscriptionCreate(BaseModel):
    user_id: int
    package_id: int
    plan_id: int
    approved_by: int
    status: str


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    package_id: int
    plan_id: int
    status: str
    start_date: datetime
    end_date: datetime | None

    package: PackageResponse | None = None
    plan: PlanResponse | None = None

    class Config:
        from_attributes = True