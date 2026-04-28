from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    stock: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True