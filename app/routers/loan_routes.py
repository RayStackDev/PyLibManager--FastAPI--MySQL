from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user, get_current_admin
from app.models.user import User
from app.schemas.loan import LoanCreate, LoanResponse
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse)
def create_loan(
    loan: LoanCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    
    if current_user.is_blocked:
        raise HTTPException(
            status_code=403,
            detail="Operação negada. Sua conta na biblioteca está suspensa ou bloqueada"
        )
    
    if current_user.pending_fines > 0.0:
        raise HTTPException(
            status_code=403,
            detail=f"Operação Negada. Você possui multas pendentes no valor de RS {current_user.pending_fines:.2f}"
        )
    
    book_repo = BookRepository(db)
    book = book_repo.get_by_id(loan.book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    if book.stock <= 0:
        raise HTTPException(status_code=400, detail="Livro esgotado no estoque")
    
    loan_repo = LoanRepository(db)
    return loan_repo.create_loan(loan, user_id=current_user.id)

@router.get("/", response_model=List[LoanResponse])
def list_active_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
    ):
    
    repo = LoanRepository(db)
    return repo.get_ative_loans()

@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book_route(
    loan_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    loan_repo = LoanRepository(db)
    updated_loan = loan_repo.return_book(loan_id)

    if not updated_loan:
        raise HTTPException(
            status_code=400,
            detail="Emprestimo nao encontrado ou livro ja devolvido"
        )
    
    return updated_loan

@router.get("/my-loans", response_model=List[LoanResponse])
def get_logged_user_loans( 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    loan_repo = LoanRepository(db)
    loans = loan_repo.get_loans_by_user(user_id=current_user.id)

    return loans