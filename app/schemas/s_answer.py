# from typing import Optional

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.models import AnswerCombiDB
from app.schemas.s_topic import TagAndID

""" Answer """


class AnswerBase(BaseModel):
    owner_uniq_id: str
    commentar_uniq_id: str
    record_uniq_id: str


class AnswerOverviewGet(BaseModel):
    answer_uniq_id: UUID
    answer_created_at: datetime
    answer_updated_at: datetime
    #
    user_uniq_id: UUID
    user_username: str
    user_created_date: datetime
    #
    commentar_uniq_id: UUID
    commentar: str
    commentar_created_at: datetime
    commentar_updated_at: datetime
    #
    record_uniq_id: UUID
    record_filename: str
    record_created_at: datetime
    record_updated_at: datetime


def create_answer_combi_from_db_model(ac: AnswerCombiDB = None):
    if ac:
        return AnswerOverviewGet(
            answer_uniq_id=str(ac.ans_uniq_id),
            answer_created_at=ac.ans_created_at,
            answer_updated_at=ac.ans_updated_at,
            #
            user_uniq_id=str(ac.u_uniq_id),
            user_username=ac.u_username,
            user_created_date=ac.u_created_at,
            #
            #
            record_uniq_id=str(ac.rc_uniq_id),
            record_filename=ac.rc_filename,
            record_created_at=ac.rc_created_at,
            record_updated_at=ac.rc_updated_at,
            #
            commentar_uniq_id=str(ac.c_uniq_id),
            commentar=ac.c_commentar,
            commentar_created_at=ac.c_created_at,
            commentar_updated_at=ac.c_updated_at
        )
    return None


# Properties to receive via API on creation
class AnswerCreate(AnswerBase):
    topic_uniq_id: UUID
    pass


# Properties to receive via API on update
class AnswerUpdate(AnswerBase):
    uniq_id: str


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
