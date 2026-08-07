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