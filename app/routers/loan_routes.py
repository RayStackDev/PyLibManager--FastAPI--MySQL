from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.loan import LoanCreate, LoanResponse
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book_repo = BookRepository(db)

    book = book_repo.get_by_id(loan.book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    if book.stock <= 0:
        raise HTTPException(status_code=400, detail="Livro esgotado no estoque")
    

    loan_repo = LoanRepository(db)
    return loan_repo.create_loan(loan)

@router.get("/", response_model=List[LoanResponse])
def list_active_loans(db: Session = Depends(get_db)):
    repo = LoanRepository(db)
    return repo.get_ative_loans()

@router.post("/{loan_id}/return", response_model=LoanResponse)
def return_book_route(loan_id: int, db: Session = Depends(get_db)):
    loan_repo = LoanRepository(db)

    updated_loan = loan_repo.return_book(loan_id)

    if not updated_loan:
        raise HTTPException(
            status_code=400,
            detail="Emprestimo nao encontrado ou livro ja devolvido"
        )
    
    return updated_loan

@router.get("/user/{user_id}", response_model=List[LoanResponse])
def get_user_loans_route(user_id: int, db: Session = Depends(get_db)):
    loan_repo = LoanRepository(db)
    loans = loan_repo.get_loans_by_user(user_id)
    return loans