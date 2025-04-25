from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from services.auth_service import AuthService
from database import models
from pydantic import BaseModel, EmailStr
import uuid, datetime
from database.auth import get_password_hash
from typing import List
from components.schemas import UserOut, TokenResponse
from database.auth import create_access_token

router = APIRouter()

# --- Schemas ---
class RoleCreate(BaseModel):
    role_name: str
    description: str = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    UserId: int
    Username: str
    Email: str
    IsActive: bool

    class Config:
        orm_mode = True

class LoginResponse(TokenResponse):
    user: UserOut

class ReportCreate(BaseModel):
    report_name: str
    report_url: str
    owner_id: int
    
class ReportOut(BaseModel):
    ReportId: int
    ReportName: str
    ReportUrl: str
    OwnerId: int
    CreatedAt: datetime.datetime

class AssignRole(BaseModel):
    user_id: int
    role_id: int

class AssignReport(BaseModel):
    role_id: int
    report_id: int

class TokenCreate(BaseModel):
    user_id: int
    expires_minutes: int

# --- Auth endpoint ---
class LoginRequest(BaseModel):
    Username: str
    PasswordHash: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    # autentica y obtiene user
    user = AuthService.authenticate_user(db, request.Username, request.PasswordHash)
    token = create_access_token({"sub": str(user.UserId)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

# --- CRUD Endpoints ---
@router.post("/roles/", status_code=201)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    role = models.Role(RoleName=payload.role_name, Description=payload.description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.post("/users/", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    hash = get_password_hash(payload.password)
    user = models.User(Username=payload.username, Email=payload.email,
                       PasswordHash=hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/users/assign-role/", status_code=201)
def assign_role(payload: AssignRole, db: Session = Depends(get_db)):
    user = db.query(models.User).get(payload.user_id)
    role = db.query(models.Role).get(payload.role_id)
    if not user or not role:
        raise HTTPException(status_code=404, detail="Usuario o Rol no encontrado")
    user.roles.append(role)
    db.commit()
    return {"msg": "Rol asignado"}

@router.post("/reports/", status_code=201)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    report = models.PowerBIReport(ReportName=payload.report_name, ReportUrl=payload.report_url, OwnerId=payload.owner_id)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/reports/", response_model=List[ReportOut])
def list_reports(db: Session = Depends(get_db)):
    return db.query(models.PowerBIReport).all()

@router.get("/reports/owner/{owner_id}", response_model=List[ReportOut])
def get_reports_by_owner(owner_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.PowerBIReport)
          .filter(models.PowerBIReport.OwnerId == owner_id)
          .all()
    )
@router.post("/roles/assign-report/", status_code=201)
def assign_report(payload: AssignReport, db: Session = Depends(get_db)):
    role = db.query(models.Role).get(payload.role_id)
    report = db.query(models.PowerBIReport).get(payload.report_id)
    if not role or not report:
        raise HTTPException(status_code=404, detail="Rol o Reporte no encontrado")
    role.reports.append(report)
    db.commit()
    return {"msg": "Reporte asignado al rol"}

@router.post("/tokens/", status_code=201)
def create_refresh_token(payload: TokenCreate, db: Session = Depends(get_db)):
    token_str = str(uuid.uuid4())
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=payload.expires_minutes)
    token = models.RefreshToken(TokenId=uuid.uuid4(), UserId=payload.user_id,
                                Token=token_str, ExpiresAt=expires)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token