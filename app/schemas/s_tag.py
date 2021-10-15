from typing import Optional

from pydantic import BaseModel, EmailStr


""" Tag """
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

""" TagTopic """
# Shared properties
class TagTopicBase(BaseModel):
    topic_id: int
    tag_id: int


# Properties to receive via API on creation
class TagTopicCreate(TagTopicBase):
    pass


# Properties to receive via API on update
class TagTopicUpdate(TagTopicBase):
    pass


class TagTopicInDBBase(TagTopicBase):
    pass
    class Config:
        orm_mode = True

