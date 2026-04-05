from sqlalchemy import Column, Integer, String, Boolean, Float
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    is_blocked = Column(Boolean, default=False)
    pending_fines = Column(float, default=0.0)