from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.book import BookCreate, BookResponse
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService

router = APIRouter(prefix="/book", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
def list_book(
    skip: int = Query(0, ge=0, description="Numero de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade maxima de registros por pagina"),
    db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    return repo.get_all()

@router.get("/search", response_model=List[BookResponse])
def search_books_route(query: str = Query(..., min_length=1, description="Termo de busca"), db: Session = Depends(get_db)):
    book_repo = BookRepository(db)
    books = book_repo.search_books(query)
    return books

@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    service = BookService(db)
    return service.create_book(book)

@router.delete("/{book_id}")
def delete_book_route(
    book_id: int, 
    db: Session = Depends(get_db),
    current_admin: User =  Depends(get_current_admin)
):
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

@router.get("/inventory-report")
def get_inventory_report(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    repo = BookRepository(db)
    books = repo.get_all(skip=0, limit=1000)

    report = []
    for book in books:
        if book.stock == 0:
            status_estoque = "Esgotado"
        elif book.stock <= 2:
            status_estoque = "Critico (Necessita Reposição)"
        else:
            status_estoque = "Estavel"
        
        report.append({
            "book_id": book.id,
            "title": book.title,
            "isbn": book.isbn,
            "current_stock": book.stock,
            "status": status_estoque
        })
    
    return report
