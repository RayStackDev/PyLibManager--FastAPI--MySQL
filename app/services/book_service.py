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
        
        return self.book_repo.create(book_data)