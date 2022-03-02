# from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class TagDB(Base):
    __tablename__ = 'tags'
    id = Column(Integer, autoincrement=True)
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_name = Column(String, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class TagTopicDB(Base):
    __tablename__ = 'tag_topic'
    id = Column(Integer, autoincrement=True)
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    tag_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("tags.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class RecordDB(Base):
    __tablename__ = 'records'
    id = Column(Integer, autoincrement=True)
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class ReadTextDB(Base):
    __tablename__ = 'read_texts'
    id = Column(Integer, autoincrement=True)
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    read_text = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class CommentarDB(Base):
    __tablename__ = 'commentars'
    id = Column(Integer, autoincrement=True)
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    commentar = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

