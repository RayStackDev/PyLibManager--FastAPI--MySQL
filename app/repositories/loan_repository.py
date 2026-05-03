from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.book import Book
from app.schemas.loan import LoanCreate
from datetime import date

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_loan(self, loan_data: LoanCreate):
        db_loan = Loan(
            user_id=loan_data.user_id,
            book_id=loan_data.book_id,
            loan_date=date.today()
        )

        book = self.db.query(Book).filter(Book.id == loan_data.book_id).first()
        if book and book.stock > 0:
            book.stock -= 1

        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan
    
    def get_ative_loans(self):
        return self.db.query(Loan).filter(Loan.return_date == None).all()
        
        