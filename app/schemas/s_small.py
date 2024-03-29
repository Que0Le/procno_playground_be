from datetime import datetime
from typing import Optional, Any, Tuple
from pydantic import BaseModel
from uuid import UUID


""" Tags """


class TagBase(BaseModel):
    tag_name: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class TagCreate(TagBase):
    tag_name: str
    description: str


# Properties to receive via API on update
class TagUpdate(TagBase):
    tag_name: str
    description: str


class TagInDBBase(TagBase):
    uniq_id: UUID
    tag_name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TagGet(TagInDBBase):
    pass

class TagTopicBase(BaseModel):
    topic_uniq_id: Optional[UUID]
    tag_uniq_id: Optional[UUID]


# Properties to receive via API on creation
class TagTopicCreate(TagTopicBase):
    topic_uniq_id: UUID
    tag_uniq_id: UUID


# Properties to receive via API on update
class TagTopicUpdate(TagTopicBase):
    pass

class TagTopicGet():
    """_summary_

    :param topic_uniq_id: _description_
    :type topic_uniq_id: UUID
    :param title: _description_
    :type title: str
    :param tag_uniq_id: _description_
    :type tag_uniq_id: UUID
    :param tag_name: _description_
    :type tag_name: str
    :param tag_description: _description_
    :type tag_description: str
    :param created_at: _description_
    :type created_at: datetime
    """

    def __init__(
        self, topic_uniq_id: UUID, title: str, tag_uniq_id: UUID, 
        tag_name: str, tag_description: str, created_at: datetime, updated_at: datetime
    ) -> None:
        self.topic_uniq_id = topic_uniq_id
        self.title = title
        self.tag_uniq_id = tag_uniq_id
        self.tag_name = tag_name
        self.tag_description = tag_description
        self.created_at = created_at
        self.updated_at = updated_at

    topic_uniq_id: UUID
    title: str
    tag_uniq_id: UUID
    tag_name: str
    tag_description: str
    created_at: datetime
    updated_at: datetime

""" Role """


class RoleBase(BaseModel):
    role_name: str
    description: str


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


class RoleGet(RoleInDBBase):
    uniq_id: UUID
    created_at: datetime
    updated_at: datetime

class RoleInDB(RoleInDBBase):
    uniq_id: UUID
    id: int
    created_at: datetime
    updated_at: datetime


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
    :param role_desciption: _description_
    :type role_desciption: str
    :param created_at: _description_
    :type created_at: datetime
    """

    def __init__(
        self, user_uniq_id: UUID, username: str,
        role_uniq_id: UUID, role_name: str, role_desciption: str, created_at: datetime
    ) -> None:

        self.user_uniq_id = user_uniq_id
        self.username = username
        self.role_uniq_id = role_uniq_id
        self.role_name = role_name
        self.role_desciption = role_desciption
        self.created_at = created_at

    user_uniq_id: UUID
    username: str
    role_uniq_id: UUID
    role_name: str
    role_desciption: str
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
    owner_uniq_id: Optional[UUID]
    filename: Optional[str]


# Properties to receive via API on creation
class RecordCreate(RecordBase):
    owner_uniq_id: UUID
    filename: str


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    uniq_id: UUID
    owner_uniq_id: UUID
    filename: str

class RecordInDBBase(RecordBase):
    uniq_id: UUID
    owner_uniq_id: UUID
    filename: str

    class Config:
        orm_mode = True


class RecordGet(RecordInDBBase):
    created_at: datetime
    updated_at: datetime


""" Commentar """


class CommentarBase(BaseModel):
    owner_uniq_id: Optional[UUID]
    commentar: Optional[str]


# Properties to receive via API on creation
class CommentarCreate(CommentarBase):
    owner_uniq_id: UUID
    commentar: str


# Properties to receive via API on update
class CommentarUpdate(CommentarBase):
    owner_uniq_id: UUID
    commentar: str


class CommentarInDBBase(CommentarBase):
    uniq_id: UUID
    owner_uniq_id: UUID
    commentar: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentarGet(CommentarInDBBase):
    pass


""" ReadText """


class ReadTextBase(BaseModel):
    owner_uniq_id: Optional[UUID]
    read_text: Optional[str]


# Properties to receive via API on creation
class ReadTextCreate(ReadTextBase):
    owner_uniq_id: UUID
    read_text: str


# Properties to receive via API on update
class ReadTextUpdate(ReadTextBase):
    read_text: str


class ReadTextInDBBase(ReadTextBase):
    uniq_id: UUID
    owner_uniq_id: UUID
    read_text: str
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True


class ReadTextGet(ReadTextInDBBase):
    pass