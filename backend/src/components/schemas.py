# schemas.py
from pydantic import BaseModel, EmailStr
import datetime

class UserOut(BaseModel):
    UserId: int
    Username: str
    Email: EmailStr
    IsActive: bool

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(TokenResponse):
    user: UserOut

class ReportOut(BaseModel):
    ReportId: int
    ReportName: str
    ReportUrl: str
    OwnerId: int
    CreatedAt: datetime.datetime

    class Config:
        orm_mode = True
