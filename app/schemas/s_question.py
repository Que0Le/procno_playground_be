from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


""" Question """


class QuestionMetaBase(BaseModel):
    topic_uniq_id: Optional[UUID]
    owner_uniq_id: Optional[UUID]
    commentar_uniq_id: Optional[UUID]
    record_uniq_id: Optional[UUID]
    read_text_uniq_id: Optional[UUID]


# Properties to receive via API on creation
class QuestionMetaCreate(QuestionMetaBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID


# Properties to receive via API on update
class QuestionMetaUpdate(QuestionMetaBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID


class QuestionMetaInDBBase(QuestionMetaBase):
    uniq_id: UUID
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID
    read_text_uniq_id: UUID
    class Config:
        orm_mode = True


class QuestionMetaGet(QuestionMetaInDBBase):
    pass

from app.schemas import s_small  
class QuestionCombineGet(BaseModel):
    question: QuestionMetaGet = None
    read_text: s_small.ReadTextGet = None
    record: s_small.RecordGet = None
    commentar: s_small.CommentarGet = None



