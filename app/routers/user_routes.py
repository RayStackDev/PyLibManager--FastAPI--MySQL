from fastapi import APIRouter, Depends, HTTPException
from app.core.security import SecurityUtils
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    db_user = repo.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado no sistema")

    user.password = SecurityUtils.generate_password_hash(user.password)

    return repo.create(user)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Ação não permitida. Você só pode visualizar o seu própio perfil."
        )
    
    repo = UserRepository(db)
    db_user = repo.get_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int, user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)

    updated_user = repo.update_user(user_id, user_data.model_dump())

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    
    return updated_user
    
@router.put("/{user_id}/block", response_model=UserResponse)
def block_user_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    repo = UserRepository(db)
    updated_user = repo.update_user(user_id, {"is_blocked": True})

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    
    return updated_user

@router.put("/{user_id}/unblock", response_model=UserResponse)
def unblock_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    repo = UserRepository(db)
    updated_user = repo.update_user(user_id, {"is_blocked": False})

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrando")
    
    return updated_user