from sqlalchemy.orm import Session

from server.database.models import User


class UserRepository:

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def delete(db: Session, user: User):
        db.delete(user)
        db.commit()