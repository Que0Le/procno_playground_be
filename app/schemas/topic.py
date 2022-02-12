from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

""" Topic """


class TopicBase(BaseModel):
    title: str
    source_language: str
    source_level: str
    wish_correct_languages: list = [str]


# Properties to receive via API on creation
class TopicCreate(TopicBase):
    pass


# Properties to receive via API on update
class TopicUpdate(TopicBase):
    pass


class TopicInDBBase(TopicBase):
    id: int
    owner_id: int
    question_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
