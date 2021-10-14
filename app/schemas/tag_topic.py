from typing import Optional

from pydantic import BaseModel, EmailStr


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