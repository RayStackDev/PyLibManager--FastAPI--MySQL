from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.schemas.loan import LoanCreate
from datetime import date, timedelta

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_loan(self, loan_data: LoanCreate, user_id: int):
        today = date.today()
        data_devolucao_prevista = today + timedelta(days=14)

        db_loan = Loan(
            user_id=user_id,
            book_id=loan_data.book_id,
            loan_date= today,
            due_date=data_devolucao_prevista
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
    
    def return_book(self, loan_id: int):
        db_loan = self.db.query(Loan).filter(
            Loan.id == loan_id,
            Loan.return_date == None
        ).first()

        if db_loan:
            today = date.today()
            db_loan.return_date = today

            if today > db_loan.due_date:
                dias_atraso = (today - db_loan.due_date).days
                valor_multa_diaria = 2.00
                total_multa = dias_atraso * valor_multa_diaria

                usuario = self.db.query(User).filter(User.id == db_loan.user_id).first()
                if usuario:
                    usuario.pending_fines += total_multa

                    
            book = self.db.query(Book).filter(Book.id == db_loan.book_id).first()
            if book:
                book.stock += 1
            
            self.db.commit()
            self.db.refresh(db_loan)
            return db_loan
        
        return None
    
    def get_loans_by_user(self, user_id: int):
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()