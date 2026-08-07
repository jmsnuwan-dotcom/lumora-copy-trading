import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from decimal import Decimal

from server.database.db import SessionLocal
from server.database.models import Package, Plan


def seed():
    db = SessionLocal()

    try:
        if db.query(Package).count() == 0:

            gold = Package(
                name="Gold",
                lot_size=Decimal("0.01"),
            )

            platinum = Package(
                name="Platinum",
                lot_size=Decimal("0.05"),
            )

            db.add_all([gold, platinum])
            db.commit()

            db.refresh(gold)
            db.refresh(platinum)

            plans = [

                Plan(
                    package_id=gold.id,
                    name="Trial",
                    duration_days=1,
                    price=Decimal("0.00"),
                ),

                Plan(
                    package_id=gold.id,
                    name="Monthly",
                    duration_days=30,
                    price=Decimal("15.00"),
                ),

                Plan(
                    package_id=gold.id,
                    name="Lifetime",
                    duration_days=None,
                    price=Decimal("99.00"),
                ),

                Plan(
                    package_id=platinum.id,
                    name="Trial",
                    duration_days=1,
                    price=Decimal("0.00"),
                ),

                Plan(
                    package_id=platinum.id,
                    name="Monthly",
                    duration_days=30,
                    price=Decimal("30.00"),
                ),

                Plan(
                    package_id=platinum.id,
                    name="Lifetime",
                    duration_days=None,
                    price=Decimal("199.00"),
                ),
            ]

            db.add_all(plans)
            db.commit()

            print("✅ Seed completed.")

        else:
            print("Database already seeded.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()