import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# ===========================
# Server
# ===========================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
)

EMAIL = os.getenv("EMAIL", "")
PASSWORD = os.getenv("PASSWORD", "")


# ===========================
# MT5
# ===========================

MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")


# ===========================
# Client
# ===========================

POLL_INTERVAL = 2
HEARTBEAT_INTERVAL = 30

DEVIATION = 20

# ===========================
# Risk Management
# ===========================

SL_POINTS = 500
RR = 1.5