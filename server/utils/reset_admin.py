from sqlalchemy.orm import Session

from server.database.db import SessionLocal
from server.database.models.user import User
from server.utils.security import hash_password


db: Session = SessionLocal()

try:
    user = (
        db.query(User)
        .filter(User.email == "admin@lumora.com")
        .first()
    )

    if user is None:
        print("Admin user not found.")
    else:
        user.password_hash = hash_password("Admin@123")
        db.commit()


finally:
    db.close()