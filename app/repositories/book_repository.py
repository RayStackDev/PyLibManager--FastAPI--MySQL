from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Book).all()
    
    def get_by_isbn(self, isbn: str):
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def create(self, book: BookCreate):
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book