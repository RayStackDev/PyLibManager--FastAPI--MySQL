from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate

class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)

    def create_book(self, book_data: BookCreate):
        if self.book_repo.get_by_isbn(book_data.isbn):
            raise HTTPException(status_code=400, detail="ISBN já cadastrado")
        
        if book_data.stock < 0:
            raise HTTPException(
                status_code=400,
                detail="O estoque inicial do livro não pode ser menor que zero."
            )
        
        ano_atual = datetime.now().year
        if book_data.publication_year > ano_atual:
            raise HTTPException(
                status_code=400,
                detail=f"Ano de publicação invalido. O livro não pode ter sido publicado no futuro (ano atual: {ano_atual})."
            )
        
        return self.book_repo.create(book_data)