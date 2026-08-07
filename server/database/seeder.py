
from decimal import Decimal

from sqlalchemy.orm import Session

from server.database.models import Package, Plan


def seed_database(db: Session):

    if db.query(Package).count() > 0:
        return

    basic = Package(
        name="Basic",
        lot_size=Decimal("0.01"),
        trades_per_signal=1,
    )

    pro = Package(
        name="Pro",
        lot_size=Decimal("0.05"),
        trades_per_signal=3,
    )

    db.add_all([basic, pro])
    db.commit()

    db.refresh(basic)
    db.refresh(pro)

    plans = [
        Plan(
            package_id=basic.id,
            name="Monthly",
            duration_days=30,
            price=Decimal("15.00"),
        ),
        Plan(
            package_id=basic.id,
            name="Lifetime",
            duration_days=None,
            price=Decimal("99.00"),
        ),
        Plan(
            package_id=pro.id,
            name="Monthly",
            duration_days=30,
            price=Decimal("49.00"),
        ),
        Plan(
            package_id=pro.id,
            name="Lifetime",
            duration_days=None,
            price=Decimal("199.00"),
        ),
    ]

    db.add_all(plans)
    db.commit()