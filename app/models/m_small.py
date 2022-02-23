# from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


# class TagBase(Base):
#     __tablename__ = 'tags'
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     tag_name = Column(String, index=True)
#     description = Column(String, unique=False, index=False, nullable=False)


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


# class TagCreate(Base):
#     # __tablename__ = 'tags'
#     tag_name = Column(String, index=True)
#     description = Column(String, unique=False, index=False, nullable=False)


# class TagTopicDB(Base):
#     __tablename__ = 'tag_topic'
#
#     # fake table to work around the sqlalchemy constraint
#     id = Column(Integer)
#     topic_uniq_id = Column(Integer, ForeignKey("topics.uniq_id"))
#     tag_uniq_id = Column(Integer, ForeignKey("tags.uniq_id"))
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class RecordDB(Base):
#     __tablename__ = 'records'
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     id = Column(Integer)
#     owner_uniq_id = Column(Integer, ForeignKey("users.uniq_id"))
#     filename = Column(String, unique=True, nullable=False)
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class RecordCreate(Base):
#     __tablename__ = 'records'
#     owner_uniq_id = Column(Integer, ForeignKey("users.uniq_id"))
#     filename = Column(String, unique=True, nullable=False)
#
#
# class RoleDB(Base):
#     __tablename__ = 'roles'
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     id = Column(Integer)
#     role_name = Column(String, index=True, nullable=False)
#     description = Column(String)
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class UserRoleDB(Base):
#     __tablename__ = 'user_role'
#
#     # fake table to work around the sqlalchemy constraint
#     id = Column(Integer)
#     user_uniq_id = Column(Integer, ForeignKey("users.uniq_id"))
#     role_uniq_id = Column(Integer, ForeignKey("roles.uniq_id"))
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class CommentarDB(Base):
#     __tablename__ = 'commentars'
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     id = Column(Integer)
#     owner_uniq_id = Column(String, ForeignKey("users.uniq_id"))
#     commentar = Column(String)
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class CommentarCreate(Base):
#     __tablename__ = 'commentars'
#
#     owner_uniq_id = Column(String, ForeignKey("users.uniq_id"))
#     commentar = Column(String)
#
#
# class ReadTextDB(Base):
#     __tablename__ = 'read_texts'
#     uniq_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     id = Column(Integer)
#     owner_uniq_id = Column(String, ForeignKey("users.uniq_id"))
#     read_text = Column(String)
#     created_at = Column(DateTime(), nullable=False)
#     updated_at = Column(DateTime(), nullable=False)
#
#
# class ReadTextCreate(Base):
#     __tablename__ = 'read_texts'
#
#     owner_uniq_id = Column(String, ForeignKey("users.uniq_id"))
#     read_text = Column(String)
