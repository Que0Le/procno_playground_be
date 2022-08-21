# from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import FetchedValue

class RoleDB(Base):
    __tablename__ = 'roles'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, server_default=FetchedValue())#, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    role_name = Column(String, nullable=False, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class UserRoleDB(Base):
    __tablename__ = 'user_role'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    user_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    role_uniq_id = Column(UUID(as_uuid=True), ForeignKey("roles.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class TagDB(Base):
    __tablename__ = 'tags'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    tag_name = Column(String, nullable=False, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class TagTopicDB(Base):
    __tablename__ = 'tag_topic'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    topic_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    tag_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("tags.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class RecordDB(Base):
    __tablename__ = 'records'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    filename = Column(String, nullable=False)
    is_uploaded = Column(Boolean(), default=False, server_default=FetchedValue())
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class ReadTextDB(Base):
    __tablename__ = 'read_texts'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    read_text = Column(String, nullable=False)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())


class CommentarDB(Base):
    __tablename__ = 'commentars'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=FetchedValue())
    id = Column(Integer, autoincrement=True, server_default=FetchedValue())
    commentar = Column(String, nullable=False)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime(), nullable=False, server_default=FetchedValue())

