from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.schemas.package import (
    PackageCreate,
    PackageResponse,
)
from server.services.package_service import PackageService
from server.database.models.user import User
from server.utils.dependencies import get_current_user
from server.services.subscription_service import SubscriptionService

router = APIRouter(
    prefix="/packages",
    tags=["Packages"],
)


@router.post(
    "",
    response_model=PackageResponse,
)
def create_package(
    request: PackageCreate,
    db: Session = Depends(get_db),
):

    try:
        return PackageService.create(
            db=db,
            request=request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get(
    "",
    response_model=list[PackageResponse],
)
def get_packages(
    db: Session = Depends(get_db),
):

    return PackageService.get_all(db)

@router.put(
    "/{package_id}",
    response_model=PackageResponse,
)
def update_package(
    package_id: int,
    request: PackageCreate,
    db: Session = Depends(get_db),
):

    try:
        return PackageService.update(
            db=db,
            package_id=package_id,
            request=request,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.delete(
    "/{package_id}",
)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
):

    try:
        return PackageService.delete(
            db=db,
            package_id=package_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.get(
    "/me",
    response_model=PackageResponse,
)
def get_my_package(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    subscription = SubscriptionService.get_active_by_user(
        db,
        current_user.id,
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="No active subscription.",
        )

    package = PackageService.get_by_id(
        db,
        subscription.package_id,
    )

    if package is None:
        raise HTTPException(
            status_code=404,
            detail="Package not found.",
        )

    return package