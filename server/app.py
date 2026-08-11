from contextlib import asynccontextmanager
from server.routes.auth import router as auth_router

from fastapi import FastAPI
from server.routes.package import router as package_router
from server.routes.user import router as user_router
from server.routes.subscription import router as subscription_router
from server.routes.dashboard import router as dashboard_router
from server.routes.connection import router as connection_router
from server.routes.symbol_mapping import router as symbol_mapping_router
from server.routes.heartbeat import router as heartbeat_router
from server.routes.trade import router as trade_router
from server.routes.ws import router as ws_router
from server.routes.plan import router as plan_router
from server.database.db import Base, engine
from server.database.db import SessionLocal
from server.database.seeder import seed_database
from server.routes.admin import router as admin_router
from server.routes.signal import router as signal_router
from server.routes.signal_delivery import router as signal_delivery_router

APP_NAME = "Lumora Copy Trading Platform"
APP_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("Server Starting...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_database(db)
    finally:
        db.close()

    print("=" * 60)

    yield

    print("=" * 60)
    print("Server Stopped")
    print("=" * 60)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
)

app.include_router(
    symbol_mapping_router,
    prefix="/symbol-mappings",
    tags=["Symbol Mappings"],
)

app.include_router(auth_router)
app.include_router(package_router)
app.include_router(plan_router)
app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(admin_router)
app.include_router(dashboard_router)
app.include_router(connection_router)
app.include_router(heartbeat_router)
app.include_router(trade_router)
app.include_router(signal_router)
app.include_router(signal_delivery_router)
app.include_router(ws_router)


@app.get("/")
async def root():
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }