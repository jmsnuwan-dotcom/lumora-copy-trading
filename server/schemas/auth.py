from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str
    package_id: int
    plan_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"