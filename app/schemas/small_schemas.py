from typing import Optional

from pydantic import BaseModel, EmailStr


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

""" UserRole """
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

""" Record """
class RecordBase(BaseModel):
    owner_id: int
    filename: str


# Properties to receive via API on creation
class RecordCreate(RecordBase):
    pass


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    pass


class RecordInDBBase(RecordBase):
    pass
    class Config:
        orm_mode = True

""" ReadText """
class ReadTextBase(BaseModel):
    owner_id: int
    read_text: str


# Properties to receive via API on creation
class ReadTextCreate(ReadTextBase):
    pass


# Properties to receive via API on update
class ReadTextUpdate(ReadTextBase):
    pass


class ReadTextInDBBase(ReadTextBase):
    pass
    class Config:
        orm_mode = True

""" Commentar """
class CommentarBase(BaseModel):
    owner_id: int
    read_text: str


# Properties to receive via API on creation
class CommentarCreate(CommentarBase):
    pass


# Properties to receive via API on update
class CommentarUpdate(CommentarBase):
    pass


class CommentarInDBBase(CommentarBase):
    pass
    class Config:
        orm_mode = True