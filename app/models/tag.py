from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, DateTime
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
            f"Tag:\nid[{str(self.id)}]\
            \ntag_name[{str(self.tag_name)}]\n\
            description[{str(self.description)}]\
            \ncreated_at[{str(self.created_at)}]\
            \nupdated_at[{str(self.updated_at)}]")
