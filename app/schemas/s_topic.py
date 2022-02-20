from typing import List
from datetime import datetime

from pydantic import BaseModel
from uuid import UUID

from app.models.m_topic import TopicCombiDB


class TagAndID(BaseModel):
    tag_uniq_id: str
    tag: str
    # def __init__(self, id, tag):
    #     self.tag_id = id
    #     self.tag = tag


class TopicGet(BaseModel):
    __slots__ = [
        'uniq_id', 'owner_uniq_id', 'title',
        'source_language', 'source_level',
        'wish_correct_languages',
        'created_at', 'updated_at'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    uniq_id: UUID
    owner_uniq_id: UUID
    title: str
    source_language: str
    source_level: str
    wish_correct_languages: List[str]
    created_at: datetime
    updated_at: datetime


""" TopicOverview """


class TopicOverviewGet(BaseModel):
    # topic_id: str
    topic_uniq_id: str
    topic_title: str
    source_language: str
    source_level: str
    wish_correct_languages: List[str]
    topic_created_at: datetime
    topic_updated_at: datetime
    #
    owner_uniq_id: str
    owner_username: str
    #
    nbr_answer: int
    #
    tag_and_uniq_id_s: List[TagAndID] = None
    #
    question_uniq_id: str
    question_created_at: datetime
    question_updated_at: datetime
    #
    readtext_uniq_id: str
    readtext: str
    readtext_created_at: datetime
    readtext_updated_at: datetime
    #
    record_uniq_id: str
    record_filename: str
    record_created_at: datetime
    record_updated_at: datetime
    #
    commentar_uniq_id: str
    commentar: str
    commentar_created_at: datetime
    commentar_updated_at: datetime


def create_topic_combi_from_db_model(tc: TopicCombiDB = None):
    if tc:
        # print(tc.tt_tag_uuids)
        tag_and_uniq_id_s = []
        for i in range(0, len(tc.tt_tag_uuids)):
            tag_and_uniq_id_s.append(
                TagAndID(tag_uniq_id=str(tc.tt_tag_uuids[i]), tag=tc.tt_tags[i])
            )
        return TopicOverviewGet(
            # topic_id=tc.t_id,
            topic_uniq_id=str(tc.t_uniq_id),
            topic_title=tc.t_title,
            source_language=tc.t_source_language,
            source_level=tc.t_source_level,
            wish_correct_languages=tc.t_wish_correct_languages,
            topic_created_at=tc.t_created_at,
            topic_updated_at=tc.t_updated_at,
            #
            owner_uniq_id=str(tc.u_uniq_id),
            owner_username=tc.u_username,
            #
            nbr_answer=tc.nbr_answers,
            #
            tag_and_uniq_id_s=tag_and_uniq_id_s,
            #
            question_uniq_id=str(tc.q_uniq_id),
            question_created_at=tc.q_created_at,
            question_updated_at=tc.q_updated_at,
            #
            readtext_uniq_id=str(tc.rt_uniq_id),
            readtext=tc.rt_read_text,
            readtext_created_at=tc.rt_created_at,
            readtext_updated_at=tc.rt_updated_at,
            #
            record_uniq_id=str(tc.rc_uniq_id),
            record_filename=tc.rc_filename,
            record_created_at=tc.rc_created_at,
            record_updated_at=tc.rc_updated_at,
            #
            commentar_uniq_id=str(tc.c_uniq_id),
            commentar=tc.c_commentar,
            commentar_created_at=tc.c_created_at,
            commentar_updated_at=tc.c_updated_at
        )

    return None


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
