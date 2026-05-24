from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.loan import LoanCreate, LoanResponse
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    db_book = book_repo.get_all()

    book = next((b for b in db_book if b.id == loan.book_id), None)

    if not book:
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    if book.stock:
        raise HTTPException(status_code=400, detail="Livro esgotado no estoque")
    

    loan_repo = LoanRepository(db)
    return loan_repo.create_loan(loan)

@router.get("/", response_model=List[LoanResponse])
def list_active_loans(db: Session = Depends(get_db)):
    repo = LoanRepository(db)
    return repo.get_ative_loans()