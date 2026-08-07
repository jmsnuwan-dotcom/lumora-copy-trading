from pathlib import Path
from dotenv import load_dotenv
import os

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# Application
# --------------------------------------------------

APP_NAME = "Lumora Copy Trading Platform"
APP_VERSION = "1.0.0"

# --------------------------------------------------
# Security
# --------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_SECRET_BEFORE_PRODUCTION"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_HOURS = 24

# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR}/storage/lumora.db"
)

# --------------------------------------------------
# WebSocket
# --------------------------------------------------

WEBSOCKET_PATH = "/ws"

# --------------------------------------------------
# Server
# --------------------------------------------------

HOST = "127.0.0.1"

PORT = 8000

DEBUG = True