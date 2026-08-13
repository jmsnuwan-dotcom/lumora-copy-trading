from sqlalchemy.orm import Session

from server.database.models import Package, Plan
from server.schemas.package import PackageCreate


class PackageService:

    @staticmethod
    def create(
        db: Session,
        request: PackageCreate,
    ):

        exists = (
            db.query(Package)
            .filter(Package.name == request.name)
            .first()
        )

        if exists:
            raise ValueError("Package already exists.")

        package = Package(
            name=request.name,
            lot_size=request.lot_size,
            trades_per_signal=request.trades_per_signal,
        )

        db.add(package)
        db.commit()
        db.refresh(package)

        monthly_plan = Plan(
            package_id=package.id,
            name="Monthly",
            duration_days=30,
            price=request.monthly_price,
        )

        lifetime_plan = Plan(
            package_id=package.id,
            name="Lifetime",
            duration_days=None,
            price=request.lifetime_price,
        )

        db.add_all([
            monthly_plan,
            lifetime_plan,
        ])

        db.commit()
        db.refresh(package)

        return package

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(Package)
            .order_by(Package.id)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        package_id: int,
        request: PackageCreate,
    ):

        package = (
            db.query(Package)
            .filter(Package.id == package_id)
            .first()
        )

        if not package:
            raise ValueError("Package not found.")

        package.name = request.name
        package.lot_size = request.lot_size
        package.trades_per_signal = request.trades_per_signal

        monthly_plan = (
            db.query(Plan)
            .filter(
                Plan.package_id == package.id,
                Plan.name == "Monthly",
            )
            .first()
        )

        if monthly_plan:
            monthly_plan.price = request.monthly_price

        lifetime_plan = (
            db.query(Plan)
            .filter(
                Plan.package_id == package.id,
                Plan.name == "Lifetime",
            )
            .first()
        )

        if lifetime_plan:
            lifetime_plan.price = request.lifetime_price

        db.commit()
        db.refresh(package)

        return package

    @staticmethod
    def delete(
        db: Session,
        package_id: int,
    ):

        package = (
            db.query(Package)
            .filter(Package.id == package_id)
            .first()
        )

        if not package:
            raise ValueError("Package not found.")

        package.is_active = False

        db.commit()

        return {
            "message": "Package disabled successfully."
        }

    @staticmethod
    def get_by_id(
        db: Session,
        package_id: int,
    ):

        return (
            db.query(Package)
            .filter(Package.id == package_id)
            .first()
        )