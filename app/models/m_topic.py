from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401

class TopicDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False, index=True)
    source_language = Column(String, nullable=False)
    source_level = Column(String, nullable=False)
    wish_correct_languages = Column(ARRAY(String, dimensions=1))
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"TopicDB:\nid[{str(self.id)}]\n\
            owner_id[{str(self.owner_id)}]\n\
            title[{str(self.title)}]\n\
            source_language[{str(self.source_language)}]\n\
            source_level[{str(self.source_level)}]\n\
            wish_correct_languages[{str(self.wish_correct_languages)}]\n\
            question_id[{str(self.question_id)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class TopicCombiDB(Base):
    # overwrite the tabble name
    __tablename__  = '__none_topic__'
    # Fake PK and indexed, cause this table is temp and generated by SQL query
    t_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    t_title = Column(String)
    t_source_language = Column(String)
    t_source_level = Column(String)
    t_wish_correct_languages = Column(String)
    t_created_at = Column(DateTime(), nullable=False)
    t_updated_at = Column(DateTime(), nullable=False)
    #
    u_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
    u_username = Column(String)
    #
    nbr_answers = Column(Integer)
    #
    tt_tag_uuids = Column(ARRAY(UUID(as_uuid=True), dimensions=1))
    tt_tags = Column(ARRAY(String, dimensions=1))
    #
    q_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
    q_created_at = Column(DateTime(), nullable=False)
    q_updated_at = Column(DateTime(), nullable=False)
    #
    rt_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
    rt_read_text = Column(String)
    rt_created_at = Column(DateTime(), nullable=False)
    rt_updated_at = Column(DateTime(), nullable=False)
    #
    rc_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
    rc_filename = Column(String)
    rc_created_at = Column(DateTime(), nullable=False)
    rc_updated_at = Column(DateTime(), nullable=False)
    #
    c_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
    c_commentar = Column(String)
    c_created_at = Column(DateTime(), nullable=False)
    c_updated_at = Column(DateTime(), nullable=False)

    # def to_string(self):
    #     return str(
    #         f"TagDB:\nt_id[{str(self.t_uniq_id)}]\n\
    #         t_title[{str(self.t_title)}]\n\
    #         t_source_language[{str(self.t_source_language)}]\n\
    #         t_source_level[{str(self.t_source_level)}]\n\
    #         t_wish_correct_languages[{str(self.t_wish_correct_languages)}]\n\
    #         t_created_at[{str(self.t_created_at)}]\n\
    #         t_updated_at[{str(self.t_updated_at)}]\n\
    #         tt_tags[{str(self.tt_tags)}]\n\
    #         nbr_answers[{str(self.nbr_answers)}]\n\
    #         q_created_at[{str(self.q_created_at)}]\n\
    #         q_updated_at[{str(self.q_updated_at)}]\n\
    #         rt_read_text[{str(self.rt_read_text)}]\n\
    #         rt_created_at[{str(self.rt_created_at)}]\n\
    #         rt_updated_at[{str(self.rt_updated_at)}]\n\
    #         rc_filename[{str(self.rc_filename)}]\n\
    #         rc_created_at[{str(self.rc_created_at)}]\n\
    #         rc_updated_at[{str(self.rc_updated_at)}]\n\
    #         c_commentar[{str(self.c_commentar)}]\n\
    #         c_created_at[{str(self.c_created_at)}]\n\
    #         c_updated_at[{str(self.c_updated_at)}]")