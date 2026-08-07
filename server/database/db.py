from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from server.config import DATABASE_URL


# ---------------------------------------
# Database Engine
# ---------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
print("DATABASE =", DATABASE_URL)

# ---------------------------------------
# Session
# ---------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ---------------------------------------
# Base Model
# ---------------------------------------

Base = declarative_base()


# ---------------------------------------
# Dependency
# ---------------------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()