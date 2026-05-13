from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.book import BookCreate, BookResponse
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/book", tags=["Books"])

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    if repo.get_by_isbn(book.isbn):
        raise HTTPException(status_code=400, detail="ISBN já cadastrado")
    return repo.create(book)

@router.get("/", response_model=List[BookResponse])
def list_book(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.get_all()
    