from sqlalchemy.orm import Session
from database import auth as auth_utils
from database import models
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, Username: str, PasswordHash: str):
        user = db.query(models.User).filter(models.User.Username == Username).first()
        if not user or not auth_utils.verify_password(PasswordHash, user.PasswordHash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        if not user.IsActive:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
        return user

    @staticmethod
    def login(db: Session, Username: str, PasswordHash: str):
        user = AuthService.authenticate_user(db, Username, PasswordHash)
        token = auth_utils.create_access_token({"sub": str(user.UserId)})
        return {"access_token": token, "token_type": "bearer"}