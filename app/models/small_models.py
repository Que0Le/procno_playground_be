from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401

class TagDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, index=True)
    description = Column(String, unique=False, index=False, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"TagDB:\nid[{str(self.id)}]\n\
            tag_name[{str(self.tag_name)}]\n\
            description[{str(self.description)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class TagTopicDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'tag_topic'

    # fake table to workaround the sqlalchemy constraint
    id = Column(Integer, primary_key=True, index=True)  
    topic_id = Column(Integer, ForeignKey("topics.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

class RecordDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will automatic generate
    __tablename__  = 'records'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"RecordDB:\nid[{str(self.id)}]\n\
            owner_id[{str(self.owner_id)}]\n\
            filename[{str(self.filename)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class RoleDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will automatic generate
    __tablename__  = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"RoleDB:\nid[{str(self.id)}]\n\
            role_name[{str(self.role_name)}]\n\
            description[{str(self.description)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class UserRoleDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'user_role'

    # fake table to workaround the sqlalchemy constraint
    id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"RoleDB:\nid[{str(self.id)}]\n\
            user_id[{str(self.user_id)}]\n\
            role_id[{str(self.role_id)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class CommentarDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will automatic generate
    __tablename__  = 'commentars'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    commentar = Column(String)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"CommentarDB:\nid[{str(self.id)}]\n\
            owner_id[{str(self.owner_id)}]\n\
            commentar[{str(self.commentar)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")

class ReadTextDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will automatic generate
    __tablename__  = 'read_texts'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    read_text = Column(String)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"ReadTextDB:\nid[{str(self.id)}]\n\
            owner_id[{str(self.owner_id)}]\n\
            read_text[{str(self.read_text)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")