from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import SecurityUtils

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(self, user_data: UserCreate):
        if len(user_data.password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Senha muito fraca. A senha deve conter pelo menos 6 caracteres."
            )
        
        db_user = self.user_repo.get_by_email(user_data.email)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Email ja cadastrado no sistema"
            )
        
        user_data.password = SecurityUtils.generate_password_hash(user_data.password)

        return self.user_repo.create(user_data)