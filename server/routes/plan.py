from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.services.plan_service import PlanService


router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


class PlanPriceUpdate(BaseModel):
    price: Decimal


@router.get(
    "/{package_id}",
)
def get_plans(
    package_id: int,
    db: Session = Depends(get_db),
):

    return PlanService.get_by_package(
        db=db,
        package_id=package_id,
    )


@router.put(
    "/price/{plan_id}",
)
def update_plan_price(
    plan_id: int,
    request: PlanPriceUpdate,
    db: Session = Depends(get_db),
):

    try:
        return PlanService.update_price(
            db=db,
            plan_id=plan_id,
            price=request.price,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )