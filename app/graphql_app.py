import binascii
import logging
from typing import List, Optional
from uuid import UUID

import graphene
import strawberry
from django.core.exceptions import ValidationError
from graphene import ObjectType
from graphql.error import GraphQLError
from graphql_relay import from_global_id

from . import models
from .database import database

APP_ID_PREFIX = "app"


def to_global_id_or_none(instance_id):
    # class_name = instance.__class__.__name__
    class_name = "ABCD"
    # print(instance)
    # if instance is None or instance.id is None:
    #     return None
    return graphene.Node.to_global_id(class_name, instance_id)


def validate_if_int_or_uuid(id):
    try:
        int(id)
    except ValueError:
        try:
            UUID(id)
        except (AttributeError, ValueError) as e:
            raise ValidationError("Must receive an int or UUID.") from e


def from_global_id_or_error(
    global_id: str,
    only_type: type[ObjectType] | str | None = None,
    raise_error: bool = False,
):
    """Resolve global ID or raise GraphQLError.

    Validates if given ID is a proper ID handled by Saleor.
    Valid IDs formats, base64 encoded:
    'app:<int>:<str>' : External app ID with 'app' prefix
    '<type>:<int>' : Internal ID containing object type and ID as integer
    '<type>:<UUID>' : Internal ID containing object type and UUID
    Optionally validate the object type, if `only_type` is provided,
    raise GraphQLError when `raise_error` is set to True.

    Returns tuple: (type, id).
    """
    logging.error("pass1")
    try:
        type_, id_ = from_global_id(global_id)
        if type_ == APP_ID_PREFIX:
            id_ = global_id
        else:
            validate_if_int_or_uuid(id_)
    except (binascii.Error, UnicodeDecodeError, ValueError, ValidationError) as e:
        if only_type:
            raise GraphQLError(
                f"Invalid ID: {global_id}. Expected: {only_type}."
            ) from e
        raise GraphQLError(f"Invalid ID: {global_id}.") from e
    if only_type and str(type_) != str(only_type):
        if not raise_error:
            return type_, None
        raise GraphQLError(
            f"Invalid ID: {global_id}. Expected: {only_type}, received: {type_}."
        )
    return type_, id_


@strawberry.type
class Author:
    id: UUID
    name: str
    bio: Optional[str]

    @strawberry.field
    async def books(self) -> List["Book"]:
        query = models.Book.__table__.select().where(models.Book.author_id == self.id)
        result = await database.fetch_all(query)
        return [
            Book(
                id=to_global_id_or_none(row.id),
                title=row.title,
                description=row.description,
                author_id=row.author_id,
            )
            for row in result
        ]


@strawberry.type
class Book:
    id: int
    title: str
    description: Optional[str]
    author_id: int

    @strawberry.field
    async def author(self) -> Optional[Author]:
        query = models.Author.__table__.select().where(
            models.Author.id == self.author_id
        )
        result = await database.fetch_one(query)
        if result:
            return Author(id=result.id, name=result.name, bio=result.bio)
        return None


@strawberry.input
class AuthorInput:
    name: str
    bio: Optional[str] = None


@strawberry.input
class BookInput:
    title: str
    description: Optional[str] = None
    author_id: int


@strawberry.type
class Query:
    @strawberry.field
    async def authors(self) -> List[Author]:
        query = models.Author.__table__.select()
        result = await database.fetch_all(query)
        return [Author(id=row.id, name=row.name, bio=row.bio) for row in result]

    @strawberry.field
    async def books(self) -> List[Book]:
        query = models.Book.__table__.select()
        result = await database.fetch_all(query)
        return [
            Book(
                id=row.id,
                title=row.title,
                description=row.description,
                author_id=row.author_id,
            )
            for row in result
        ]

    @strawberry.field
    async def author(self, id: str) -> Optional[Author]:
        type, id = from_global_id_or_error(id)
        query = models.Author.__table__.select().where(models.Author.id == id)
        result = await database.fetch_one(query)
        if result:
            return Author(id=result.id, name=result.name, bio=result.bio)
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_author(self, author: AuthorInput) -> Author:
        query = models.Author.__table__.insert().values(
            name=author.name, bio=author.bio
        )
        author_id = await database.execute(query)
        # author = models.Author.__table__.select().where(models.Author.id == author_id)
        # print(to_global_id_or_none(author))
        # logging.error(to_global_id_or_none(author))
        return Author(
            id=to_global_id_or_none(author_id), name=author.name, bio=author.bio
        )

    @strawberry.mutation
    async def create_book(self, book: BookInput) -> Book:
        query = models.Book.__table__.insert().values(
            title=book.title, description=book.description, author_id=book.author_id
        )
        book_id = await database.execute(query)
        return Book(
            id=book_id,
            title=book.title,
            description=book.description,
            author_id=book.author_id,
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
