from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    db_user = repo.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado no sistema")
    return repo.create(user)