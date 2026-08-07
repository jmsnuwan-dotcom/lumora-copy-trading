from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext

from server.config import (
    ACCESS_TOKEN_EXPIRE_HOURS,
    ALGORITHM,
    SECRET_KEY,
)

# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# --------------------------------------------------
# JWT
# --------------------------------------------------

def create_access_token(user_id: int) -> str:

    expire = datetime.now(UTC) + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )