# from typing import TYPE_CHECKING

# from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.orm import relationship

# from app.db.base_class import Base

# # if TYPE_CHECKING:
# #     from .item import Item  # noqa: F401

# class TopicDB(Base):
#     # overwrite the tabble name, otherwise sqlalchemy will assume "userdb"
#     __tablename__  = 'topics'

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     salt = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean(), default=True)
#     bio = Column(String, nullable=True, default='')
