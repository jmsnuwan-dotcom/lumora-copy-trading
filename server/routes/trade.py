from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.schemas.trade import (
    BuyTradeRequest,
    CloseTradeRequest,
    SellTradeRequest,
)
from server.services.trade_service import TradeService
from server.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/trades",
    tags=["Trades"],
)


def _ensure_admin(user) -> None:
    if getattr(user, "role", None) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )


@router.post("/buy")
async def buy_trade(
    request: BuyTradeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ensure_admin(current_user)

    await TradeService.send_trade(
        db=db,
        admin_id=current_user.id,
        action="BUY",
        symbol=request.symbol,
        trade_id=request.trade_id,
        magic_number=request.magic_number,
    )

    return {"success": True}


@router.post("/sell")
async def sell_trade(
    request: SellTradeRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ensure_admin(current_user)

    await TradeService.send_trade(
        db=db,
        admin_id=current_user.id,
        action="SELL",
        symbol=request.symbol,
        trade_id=request.trade_id,
        magic_number=request.magic_number,
    )

    return {"success": True}


@router.post("/close")
async def close_trade(
    request: CloseTradeRequest,
    db: Session =Depends(get_db),
    current_user=Depends(get_current_user),
):
    _ensure_admin(current_user)

    await TradeService.send_trade(
        db=db,
        admin_id=current_user.id,
        action="CLOSE",
        symbol="",
        trade_id=request.trade_id,
        magic_number=request.magic_number,
    )

    return {"success": True}    