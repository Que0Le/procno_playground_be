from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401

class TopicDB(Base):
    # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
    __tablename__  = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False, index=True)
    source_language = Column(String, nullable=False)
    source_level = Column(String, nullable=False)
    wish_correct_languages = Column(ARRAY(String, dimensions=1))
    question_id = Column(Integer, ForeignKey("questions.id"))
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

    def to_string(self):
        return str(
            f"TopicDB:\nid[{str(self.id)}]\n\
            owner_id[{str(self.owner_id)}]\n\
            title[{str(self.title)}]\n\
            source_language[{str(self.source_language)}]\n\
            source_level[{str(self.source_level)}]\n\
            wish_correct_languages[{str(self.wish_correct_languages)}]\n\
            question_id[{str(self.question_id)}]\n\
            created_at[{str(self.created_at)}]\n\
            updated_at[{str(self.updated_at)}]")