from typing import Optional

from pydantic import BaseModel, EmailStr


""" Answer """
class AnswerBase(BaseModel):
    owner_id: int
    commentar_id: int
    record_id: int


# Properties to receive via API on creation
class AnswerCreate(AnswerBase):
    pass


# Properties to receive via API on update
class AnswerUpdate(AnswerBase):
    pass


class AnswerInDBBase(AnswerBase):
    pass
    class Config:
        orm_mode = True

""" TopicAnswer """
# Shared properties
class TopicAnswerBase(BaseModel):
    topic_id: int
    answer_id: int


# Properties to receive via API on creation
class TopicAnswerCreate(TopicAnswerBase):
    pass


# Properties to receive via API on update
class TopicAnswerUpdate(TopicAnswerBase):
    pass


class TopicAnswerInDBBase(TopicAnswerBase):
    pass
    class Config:
        orm_mode = True