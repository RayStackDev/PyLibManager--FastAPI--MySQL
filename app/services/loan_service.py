from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.schemas.loan import LoanCreate
from app.models.user import User

class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.loan_repo = LoanRepository(db)
        self.book_repo = BookRepository(db)

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