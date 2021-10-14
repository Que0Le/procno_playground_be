from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401

class TagTopicDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'tag_topic'

    # fake table to workaround the sqlalchemy constraint
    id = Column(Integer, primary_key=True, index=True)  
    topic_id = Column(Integer, ForeignKey("topics.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)