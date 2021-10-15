from typing import Optional

from pydantic import BaseModel, EmailStr


""" Question """
class QuestionBase(BaseModel):
    owner_id: int
    commentar_id: int
    record_id: int
    text_id: int


# Properties to receive via API on creation
class QuestionCreate(QuestionBase):
    pass


# Properties to receive via API on update
class QuestionUpdate(QuestionBase):
    pass


class QuestionInDBBase(QuestionBase):
    pass
    class Config:
        orm_mode = True