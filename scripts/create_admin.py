import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from server.database.db import SessionLocal
from server.database.models import User
from server.utils.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        email = "admin@lumora.com"

        admin = db.query(User).filter(User.email == email).first()

        if admin:
            print("⚠️ Admin already exists.")
            return

        admin = User(
            full_name="Lumora Administrator",
            email=email,
            password_hash=hash_password("Admin@123"),
            role="admin",
            status="active",
            trial_used=True,
            phone_number=None,
        )

        db.add(admin)
        db.commit()

        print("✅ Admin account created.")
        print("----------------------------")
        print("Email    : admin@lumora.com")
        print("Password : Admin@123")
        print("----------------------------")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()