from typing import Optional

from pydantic import BaseModel, EmailStr


""" Question """


class QuestionBase(BaseModel):
    owner_uniq_id: str
    commentar_uniq_id: str
    record_uniq_id: str
    text_uniq_id: str


# Properties to receive via API on creation
class QuestionCreate(QuestionBase):
    pass


# Properties to receive via API on update
class QuestionUpdate(QuestionBase):
    pass


class QuestionGet(QuestionBase):
    pass


# class QuestionInDBBase(QuestionBase):
#     pass
#     class Config:
#         orm_mode = True
