from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import SecurityUtils

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: UserCreate):
        hashed_password = SecurityUtils.generate_password_hash(user.password)
        
        db_user = User(
            name=user.name, 
            email=user.email, 
            password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_data_dict: dict):
        db_user = self.get_by_id(user_id)

        if db_user:

            for key, value in user_data_dict.items():
                if value is not None:
                    setattr(db_user, key, value)
            
            self.db.commit()
            self.db. refresh(db_user)
            return db_user
        
        return None