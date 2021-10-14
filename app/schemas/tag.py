from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class TagBase(BaseModel):
    tag_name: str
    description: str


# Properties to receive via API on creation
class TagCreate(TagBase):
    pass


# Properties to receive via API on update
class TagUpdate(TagBase):
    pass


class TagInDBBase(TagBase):
    pass
    class Config:
        orm_mode = True
