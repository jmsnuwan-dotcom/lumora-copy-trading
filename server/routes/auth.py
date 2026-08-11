from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db import get_db
from server.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
)
from server.services import AuthService
from server.utils.security import create_access_token
from server.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        user = AuthService.register(
            db=db,
            full_name=request.full_name,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password,
            confirm_password=request.confirm_password,
            package_id=request.package_id,
            plan_id=request.plan_id,
        )

        token = create_access_token(user.id)

        return AuthResponse(
            message="Registration successful. Waiting for payment approval.",
            access_token=token,
        )

    except ValueError as e:
        print("REGISTER ERROR:", str(e))

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    print("EMAIL:", request.email)


    try:
        user = AuthService.login(
            db=db,
            email=request.email,
            password=request.password,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.public_id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role,
        },
        
    }

@router.get("/me")
def me(current_user=Depends(get_current_user)):

    return {
        "id": current_user.public_id,
        "name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status,
        "signals_enabled": current_user.signals_enabled,
    }