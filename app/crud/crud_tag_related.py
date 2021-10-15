from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.small_models import TagDB, TagTopicDB
from app.schemas.tag_related import (
    TagCreate, TagInDBBase, TagUpdate,
    TagTopicCreate, TagTopicUpdate
)

class CRUDTag(CRUDBase[TagDB, TagCreate, TagUpdate]):
    def get_by_tag_name(self, db: Session, *, tag_name: str) -> Optional[TagDB]:
        return db.query(TagDB).filter(TagDB.tag_name == tag_name).first()

    # def create(self, db: Session, *, obj_in: UserCreate) -> UserDB:
    #     salt = generate_salt()
    #     db_obj = UserDB(
    #         username=obj_in.username,
    #         email=obj_in.email,
    #         salt=salt,
    #         hashed_password=get_password_hash(salt + obj_in.password),
    #         bio=obj_in.bio,
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     # TODO: set role for user in DB

    #     return db_obj
 
    # def update(
    #     self, db: Session, *, db_obj: UserDB, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> UserDB:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

tag = CRUDTag(TagDB)


"""  """


class CRUDTagTopic(CRUDBase[TagTopicDB, TagTopicCreate, TagTopicUpdate]):
    def get_topic_ids_by_tag_id(self, db: Session, *, tag_id: int, skip=0, limit=100) -> Optional[List[int]]:
        return (
            db.query(TagTopicDB.topic_id)
            .filter(TagTopicDB.tag_id == tag_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # def create(self, db: Session, *, obj_in: UserCreate) -> UserDB:
    #     salt = generate_salt()
    #     db_obj = UserDB(
    #         username=obj_in.username,
    #         email=obj_in.email,
    #         salt=salt,
    #         hashed_password=get_password_hash(salt + obj_in.password),
    #         bio=obj_in.bio,
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     # TODO: set role for user in DB

    #     return db_obj

    # def update(
    #     self, db: Session, *, db_obj: UserDB, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> UserDB:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)


tag_topic = CRUDTagTopic(TagTopicDB)
