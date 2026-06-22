from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.services.loan_service import LoanService
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
    service = LoanService(db)
    return service.create_loan(loan, current_user)

@router.get("/", response_model=List[LoanResponse])
def list_active_loans(
    skip: int = Query(0, ge=0, description="Numero de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade maxima de registro por pagina"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
    ):
    
    repo = LoanRepository(db)
    return repo.get_ative_loans(skip=skip, limit=limit)

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

@router.get("/overdue", response_model=List[LoanResponse])
def list_overdue_loans(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    repo = LoanRepository(db)
    return repo.get_overdue_loans()