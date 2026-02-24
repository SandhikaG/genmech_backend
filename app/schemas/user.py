from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    phone: Optional[str]
    role: str

    class Config:
        orm_mode = True


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str

class AssignServiceSchema(BaseModel):
    engineer_user_id:int
    company_id: int
    service_name: str