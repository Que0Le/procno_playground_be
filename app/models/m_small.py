# from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID


class RoleDB(Base):
    __tablename__ = 'roles'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    role_name = Column(String, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class UserRoleDB(Base):
    __tablename__ = 'user_role'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    user_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    role_uniq_id = Column(UUID(as_uuid=True), ForeignKey("roles.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class TagDB(Base):
    __tablename__ = 'tags'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    tag_name = Column(String, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class TagTopicDB(Base):
    __tablename__ = 'tag_topic'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    topic_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    tag_uniq_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("tags.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class RecordDB(Base):
    __tablename__ = 'records'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    filename = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class ReadTextDB(Base):
    __tablename__ = 'read_texts'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    read_text = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)


class CommentarDB(Base):
    __tablename__ = 'commentars'
    uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(Integer, autoincrement=True)
    commentar = Column(String)
    owner_uniq_id = Column(UUID(as_uuid=True), ForeignKey("users.uniq_id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

