from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.topic import TopicDB
from app.schemas.topic import TopicBase, TopicCreate, TopicUpdate, TopicInDBBase


class CRUDTopic(CRUDBase[TopicDB, TopicCreate, TopicUpdate]):
    def get_all_by_topic_title(
        self, db: Session, *, title: str, skip=0, limit=100
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)
            .offset(skip)
            .limit(limit)        
            .first()
        )
    def get_one_by_topic_title(
        self, db: Session, *, title: str
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)            
            .all()
        )
    def get_one_by_topic_id(
        self, db: Session, *, id: int
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.id == id)            
            .first()
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


topic = CRUDTopic(TopicDB)
