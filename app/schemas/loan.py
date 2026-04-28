from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoanBase(BaseModel):
    user_id: int
    book_id: int

class LoanCreate(LoanBase):
    pass

class LoanResponse(LoanBase):
    id: int
    loan_date : date
    return_date: Optional[date] = None

    class Config:
        from_attributes = True