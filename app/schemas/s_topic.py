from typing import Optional
from datetime import datetime, time, timedelta

from pydantic import BaseModel, EmailStr
from uuid import UUID

from app.models.m_topic import TopicCombiDB

class TagAndID():
    tag_id: str
    tag: str
    def __init__(self, id, tag):
        self.tag_id = id
        self.tag = tag

""" TopicOverview """
class TopicOverviewGet(BaseModel):
    topic_id: str
    topic_title: str
    topic_created_at: datetime
    topic_updated_at: datetime
    #
    nbr_answer: int
    #
    # tag_ids: list=[UUID]
    # tags: list=[str]
    tag_and_ids: list
    #
    question_id: str
    question_created_at: datetime
    question_updated_at: datetime
    #
    readtext_id: str
    readtext: str
    readtext_created_at: datetime
    readtext_updated_at: datetime
    #
    record_id: str
    record_filename: str
    record_created_at: datetime
    record_updated_at: datetime
    #
    commentar_id: str
    commentar: str
    commentar_created_at: datetime
    commentar_updated_at: datetime

    # def __init__(self, tc: TopicCombiDB = None):
    #     if tc:
    #         print(tc.t_uniq_id, tc.q_uniq_id)
    #         self.topic_id = "str(tc.t_uniq_id)"
    #         self.topic_title = tc.t_title
    #         self.topic_created_at = tc.t_created_at
    #         self.topic_updated_at = tc.t_updated_at
    #         #
    #         self.nbr_answer = tc.nbr_answers
    #         #
    #         for i in range(0, len(tc.tt_tag_uuids)):
    #             self.tag_and_ids.append(
    #                 TagAndID(str(tc.tt_tag_uuids[i]), tc.tt_tags[i])
    #             )
    #         #
    #         self.question_id = str(tc.q_uniq_id)
    #         self.question_created_at = tc.q_created_at
    #         self.question_updated_at = tc.q_updated_at
    #         #
    #         self.readtext_id = str(tc.rt_uniq_id)
    #         self.readtext = tc.rt_read_text
    #         self.readtext_created_at = tc.rt_created_at
    #         self.readtext_updated_at = tc.rt_updated_at
    #         #
    #         self.record_id = str(tc.rc_uniq_id)
    #         self.record_filename = tc.rc_filename
    #         self.record_created_at = tc.rc_created_at
    #         self.record_updated_at = tc.rc_updated_at
    #         #
    #         self.commentar_id = str(tc.c_uniq_id)
    #         self.commentar = tc.c_commentar
    #         self.commentar_created_at = tc.c_created_at
    #         self.commentar_updated_at = tc.c_updated_at



class TopicCreate(BaseModel):
    # topic_id: UUID
    topic_title: str
    # topic_created_at: datetime
    # topic_updated_at: datetime
    #
    # question_id: UUID
    # question_created_at: datetime
    # question_updated_at: datetime
    #
    # readtext_id: UUID
    # readtext: str
    # readtext_created_at: datetime
    # readtext_updated_at: datetime
    #
    # record_id: UUID
    # record_filename: str
    # record_created_at: datetime
    # record_updated_at: datetime
    #
    # commentar_id: UUID
    # commentar: str
    # commentar_created_at: datetime
    # commentar_updated_at: datetime

# Properties to receive via API on creation
# class TopicOverviewCreate(TopicOverviewBase):
#     pass


# # Properties to receive via API on update
# class TopicOverviewUpdate(TopicOverviewBase):
#     pass


# class TopicOverviewInDBBase(TopicOverviewBase):
#     pass
#     class Config:
#         orm_mode = True