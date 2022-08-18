from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
# from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
import uuid

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class UserDB(Base):
    # overwrite the table name, otherwise sqlalchemy will assume "userdb"
    __tablename__ = 'users'

    id = Column(Integer)
    uniq_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    salt = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    bio = Column(String, nullable=True, default='')
    # TODO: datetime
    # TODO: do we need orm relationship here?
