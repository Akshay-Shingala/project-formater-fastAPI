from typing import List, Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List["Book"] = []

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Optional[Author] = None

    class Config:
        from_attributes = True


# Update forward references
Author.model_rebuild()
