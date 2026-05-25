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

@router.delete("/{book_id}")
def delete_book_route(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    result = repo.delete_book(book_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Livro nao encontrado")
    elif result == "has_relationships":
        raise HTTPException(
            status_code=400,
            detail="Não é possivel deletar este livro pois ele possui historico de emprestimos ativo"
        )
    
    return {"detail": "Livro deletado com sucesso"}
