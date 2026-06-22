from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.loan import Loan
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Book).offset(skip).limit(limit).all()
    
    def get_by_isbn(self, isbn: str):
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def get_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def create(self, book: BookCreate):
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
    
    def search_books(self, query: str):
        return self.db.query(Book).filter(
            (Book.title.contains(query)) | (Book.author.contains(query))).all()
    
    def delete_book(self, book_id: int):
        db_book = self.get_by_id(book_id)

        if db_book:

            has_loans = self.db.query(Loan).filter(Loan.book_id == book_id).first()
            if has_loans:
                return "has_relationships"
            
            self.db.delete(db_book)
            self.db.commit()
            return "success"
        
        return "not_found"