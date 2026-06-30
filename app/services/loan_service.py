from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.repositories.user_repository import UserRepository
from app.schemas.loan import LoanCreate
from app.models.user import User

class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)
        self.user_repo = UserRepository(db)

    def create_loan(self, loan_data: LoanCreate, current_user: User):
        if current_user.is_blocked:
            raise HTTPException(
                status_code=403,
                detail="Operação negada. Sua conta na biblioteca está suspensa ou bloqueada"
            )
        
        if current_user.pending_fines > 0.0:
            raise HTTPException(
                status_code=403,
                detail=f"Operacação negada. Você possui multas pendentes no valor de RS {current_user.pending_fines:.2f}"
            )
        
        active_loans_count = self.loan_repo.count_active_loans_by_user(current_user.id)
        if active_loans_count >= 3:
            raise HTTPException(
                status_code=400,
                detail=f"Operacação Negada. Você ja possui {active_loans_count} emprestimos ativos. O limite maximo é de 3 livros por vez."
            )
        
        book = self.book_repo.get_by_id(loan_data.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Livro nao encontrado")
        if book.stock <= 0:
            raise HTTPException(status_code=400, detail="Livro esgotado no estoque")
        
        return self.loan_repo.create_loan(loan_data, user_id=current_user.id)
    
    def return_book(self, loan_id: int):
        db_loan = self.loan_repo.return_book(loan_id)
        if not db_loan:
            return None
        
        today = date.today()
        if today > db_loan.due_date:
            dias_atraso = (today - db_loan.due_date).days
            valor_multa_diaria = 2.00
            total_multa = dias_atraso * valor_multa_diaria

            usuario = self.user_repo.get_by_id(db_loan.user_id)
            if usuario:
                self.user_repo.update_user(usuario.id, {"pending_fines": usuario.pending_fines + total_multa})

        book = self.book_repo.get_by_id(db_loan.book_id)
        if book:
            self.book_repo.db.query(book.__class__).filter(book.__class__ == book.id).update({"stock": book.stock + 1})
            self.db.commit()

        return db_loan