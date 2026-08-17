from pathlib import Path
import os

from dotenv import load_dotenv


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


# --------------------------------------------------
# Application
# --------------------------------------------------

APP_NAME = "Lumora Copy Trading Platform"
APP_VERSION = "1.0.0"


# --------------------------------------------------
# Security
# --------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is required."
    )


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 24


# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR}/storage/lumora.db",
)


# --------------------------------------------------
# WebSocket
# --------------------------------------------------

WEBSOCKET_PATH = "/ws"


# --------------------------------------------------
# Server
# --------------------------------------------------

HOST = os.getenv(
    "HOST",
    "0.0.0.0",
)

PORT = int(
    os.getenv(
        "PORT",
        "8000",
    )
)

DEBUG = os.getenv(
    "DEBUG",
    "False",
).lower() in {
    "1",
    "true",
    "yes",
}