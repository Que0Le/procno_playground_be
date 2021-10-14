from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import generate_salt, get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.tag import TagDB
from app.schemas.tag import TagCreate, TagInDBBase, TagUpdate


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
