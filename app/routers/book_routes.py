from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.book import BookCreate, BookResponse
from app.repositories.book_repository import BookRepository

router = APIRouter(prefix="/book", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
def list_book(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.get_all()

@router.get("/search", response_model=List[BookResponse])
def search_books_route(query: str = Query(..., min_length=1, description="Termo de busca"), db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    books = book_repo.search_books(query)
    return books

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    if repo.get_by_isbn(book.isbn):
        raise HTTPException(status_code=400, detail="ISBN já cadastrado")
    return repo.create(book)
