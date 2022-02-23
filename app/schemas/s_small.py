from typing import Optional

from pydantic import BaseModel, EmailStr


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














# Role
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


# UserRole
# Shared properties
class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


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


# Record
class RecordBase(BaseModel):
    owner_uniq_id: str
    filename: str


# Properties to receive via API on creation
class RecordCreate(RecordBase):
    pass


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    pass


# ReadText
class ReadTextBase(BaseModel):
    owner_uniq_id: int = None
    read_text: str = None


# Properties to receive via API on creation
class ReadTextCreate(ReadTextBase):
    pass


# Properties to receive via API on update
class ReadTextUpdate(ReadTextBase):
    uniq_id: str = None


# Commentar
class CommentarBase(BaseModel):
    owner_uniq_id: int
    read_text: str


# Properties to receive via API on creation
class CommentarCreate(CommentarBase):
    pass


# Properties to receive via API on update
class CommentarUpdate(CommentarBase):
    uniq_id: str = None


