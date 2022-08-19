from datetime import datetime
from typing import Optional, Any, Tuple
from pydantic import BaseModel
from uuid import UUID


""" Tags """
class TagBase(BaseModel):
    tag_name: str = None
    description: str = None


# Properties to receive via API on creation
class TagCreate(TagBase):
    pass


# Properties to receive via API on update
class TagUpdate(TagBase):
    uniq_id: str = None


class TagTopicBase(BaseModel):
    topic_uniq_id: str = None
    tag_uniq_id: str = None


# Properties to receive via API on creation
class TagTopicCreate(TagBase):
    pass


# Properties to receive via API on update
class TagTopicUpdate(TagBase):
    uniq_id: str = None




""" Role """
class RoleBase(BaseModel):
    role_name: str
    description: str


class RoleGet(RoleBase):
    uniq_id: UUID
    created_at: datetime


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    pass


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    pass

    class Config:
        orm_mode = True


""" UserRole """
# Shared properties
class UserRoleBase(BaseModel):
    user_id: UUID
    role_id: UUID


class UserRoleGet():
    """_summary_
    :param user_uniq_id: _description_
    :type user_uniq_id: UUID
    :param username: _description_
    :type username: str
    :param role_uniq_id: _description_
    :type role_uniq_id: UUID
    :param role_name: _description_
    :type role_name: str
    :param created_at: _description_
    :type created_at: datetime
    """

    def __init__(
        self, user_uniq_id: UUID, username: str,
        role_uniq_id: UUID, role_name: str, created_at: datetime
    ) -> None:
        self.user_uniq_id = user_uniq_id
        self.username = username
        self.role_uniq_id = role_uniq_id
        self.role_name = role_name
        self.created_at = created_at

    user_uniq_id: UUID
    username: str
    role_uniq_id: UUID
    role_name: str
    created_at: datetime


# Properties to receive via API on creation
class UserRoleCreate(UserRoleBase):
    pass


# Properties to receive via API on update
class UserRoleUpdate(UserRoleBase):
    pass


class UserRoleInDBBase(UserRoleBase):
    pass

    class Config:
        orm_mode = True


""" Record """
class RecordBase(BaseModel):
    owner_uniq_id: str
    filename: str


# Properties to receive via API on creation
class RecordCreate(RecordBase):
    pass


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    pass


""" ReadText """
class ReadTextBase(BaseModel):
    owner_uniq_id: int = None
    read_text: str = None


# Properties to receive via API on creation
class ReadTextCreate(ReadTextBase):
    pass


# Properties to receive via API on update
class ReadTextUpdate(ReadTextBase):
    uniq_id: str = None


""" Commentar """
class CommentarBase(BaseModel):
    owner_uniq_id: int
    read_text: str


# Properties to receive via API on creation
class CommentarCreate(CommentarBase):
    pass


# Properties to receive via API on update
class CommentarUpdate(CommentarBase):
    uniq_id: str = None


