from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.services.plan_service import PlanService
from server.schemas.plan import PlanResponse

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.get(
    "/{package_id}",
    response_model=list[PlanResponse],
)
def get_plans(
    package_id: int,
    db: Session = Depends(get_db),
):

    return PlanService.get_by_package(
        db=db,
        package_id=package_id,
    )