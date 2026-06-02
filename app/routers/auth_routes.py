from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.core.security import SecurityUtils

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(login_data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = SecurityUtils.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}