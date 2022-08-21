from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


""" Question """

class User(BaseModel):
    name: str = "1"

    class Config: 
        orm_mode = True

class Article(BaseModel):
    text: str = "2"
    author_id: int = "2"

    class Config:
        orm_mode = True

class ArticleResponse(BaseModel):
    article: Article
    author: User


class QuestionBase(BaseModel):
    topic_uniq_id: Optional[UUID]
    owner_uniq_id: Optional[UUID]
    commentar_uniq_id: Optional[UUID]
    record_uniq_id: Optional[UUID]
    read_text_uniq_id: Optional[UUID]


# Properties to receive via API on creation
class QuestionCreate(QuestionBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID


# Properties to receive via API on update
class QuestionUpdate(QuestionBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID


class QuestionInDBBase(QuestionBase):
    uniq_id: UUID
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID
    class Config:
        orm_mode = True


class QuestionGet(QuestionInDBBase):
    pass
