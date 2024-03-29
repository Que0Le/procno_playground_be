# from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, ARRAY
import uuid

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue


class AnswerMetaDB(Base):
    # overwrite the table name
    __tablename__ = 'answers'

    id = Column(Integer, index=True, server_default=FetchedValue())
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    topic_uniq_id = Column(UUID(as_uuid=True), ForeignKey("topics.uniq_id"))
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    commentar_uniq_id = Column(UUID(as_uuid=True), ForeignKey("commentars.uniq_id"))
    record_uniq_id = Column(UUID(as_uuid=True), ForeignKey("records.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())



# # from typing import TYPE_CHECKING

# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from app.db.base_class import Base
# from sqlalchemy.dialects.postgresql import UUID

# import uuid


# # if TYPE_CHECKING:
# #     from .item import Item  # noqa: F401


# class AnswerDB(Base):
#     # overwrite the table name
#     __tablename__ = 'answers'
#     id = Column(Integer)
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     owner_uniq_id = Column(Integer, ForeignKey("users.uniq_id"))
#     commentar_uniq_id = Column(Integer, ForeignKey("commentars.uniq_id"))
#     record_uniq_id = Column(Integer, ForeignKey("records.uniq_id"))
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)


# class AnswerCombiDB(Base):
#     # overwrite the table name
#     __tablename__ = '__none_answer_combi__'

#     # Fake PK and indexed (primary_key=True),
#     # cause this table is temporary and doesn't exist in DB
#     ans_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     ans_created_at = Column(DateTime(), nullable=False)
#     ans_updated_at = Column(DateTime(), nullable=False)
#     #
#     u_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
#     u_username = Column(String)
#     u_created_at = Column(DateTime(), nullable=False)
#     #
#     rc_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
#     rc_filename = Column(String)
#     rc_created_at = Column(DateTime(), nullable=False)
#     rc_updated_at = Column(DateTime(), nullable=False)
#     #
#     c_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4)
#     c_commentar = Column(String)
#     c_created_at = Column(DateTime(), nullable=False)
#     c_updated_at = Column(DateTime(), nullable=False)
