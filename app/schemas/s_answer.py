from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.schemas import s_small  


""" Answer """


class AnswerMetaBase(BaseModel):
    topic_uniq_id: Optional[UUID]
    owner_uniq_id: Optional[UUID]
    commentar_uniq_id: Optional[UUID]
    record_uniq_id: Optional[UUID]


# Properties to receive via API on creation
class AnswerMetaCreate(AnswerMetaBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID


# Properties to receive via API on update
class AnswerMetaUpdate(AnswerMetaBase):
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID


class AnswerMetaInDBBase(AnswerMetaBase):
    uniq_id: UUID
    topic_uniq_id: UUID
    owner_uniq_id: UUID
    commentar_uniq_id: UUID
    record_uniq_id: UUID

    class Config:
        orm_mode = True


class AnswerMetaGet(AnswerMetaInDBBase):
    pass


class AnswerCombineGet(BaseModel):
    answer: AnswerMetaGet = None
    record: s_small.RecordGet = None
    commentar: s_small.CommentarGet = None



