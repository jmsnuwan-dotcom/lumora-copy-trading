from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    status: str
    phone_number: str | None = None

    class Config:
        from_attributes = True