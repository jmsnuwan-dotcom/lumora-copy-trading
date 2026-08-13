from decimal import Decimal

from sqlalchemy.orm import Session

from server.database.models import Plan


class PlanService:

    @staticmethod
    def get_by_package(
        db: Session,
        package_id: int,
    ):

        return (
            db.query(Plan)
            .filter(
                Plan.package_id == package_id,
                Plan.is_active == True,
            )
            .order_by(Plan.id)
            .all()
        )

    @staticmethod
    def update_price(
        db: Session,
        plan_id: int,
        price: Decimal,
    ):

        plan = (
            db.query(Plan)
            .filter(Plan.id == plan_id)
            .first()
        )

        if not plan:
            raise ValueError("Plan not found.")

        plan.price = price

        db.commit()
        db.refresh(plan)

        return plan