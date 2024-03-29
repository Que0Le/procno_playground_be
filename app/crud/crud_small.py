from datetime import datetime
from typing import Optional, List
import uuid
import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.encoders import jsonable_encoder

from app.db.queries import *
from app.crud.base import CRUDBase
from app.models import m_small, m_user, m_topic
from app.schemas import *
from app.models import *
from app.schemas import s_small


# logger = logging.getLogger(__name__)

class CRUDRole(CRUDBase[m_small.RoleDB, s_small.RoleCreate, s_small.RoleUpdate]):
    def get_role_by_role_name(
        self, db: Session, *, role_name: str
    ) -> m_small.RoleDB:
        return (
            db.query(self.model)
            .filter(m_small.RoleDB.role_name == role_name)
            .first()
        )


crud_role = CRUDRole(m_small.RoleDB)


class CRUDUserRole(CRUDBase[m_small.UserRoleDB, s_small.UserRoleCreate, s_small.UserRoleUpdate]):
    def get_roles_of_user(
        self, db: Session, *, user_uniq_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[m_small.RoleDB]:
        return (
            db.query(m_small.RoleDB)
            .filter(m_user.UserDB.uniq_id == user_uniq_id)
            .filter(m_user.UserDB.uniq_id == m_small.UserRoleDB.user_uniq_id)
            .filter(m_small.RoleDB.uniq_id == m_small.UserRoleDB.role_uniq_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_user_role = CRUDUserRole(m_small.UserRoleDB)


class CRUDTag(CRUDBase[m_small.TagDB, s_small.TagCreate, s_small.TagUpdate]):
    def get_tag_by_tag_name(
        self, db: Session, *, tag_name: str
    ) -> m_small.TagDB:
        return (
            db.query(self.model)
            .filter(m_small.TagDB.tag_name == tag_name)
            .first()
        )


crud_tag = CRUDTag(m_small.TagDB)


class CRUDTagTopic(CRUDBase[m_small.TagTopicDB, s_small.TagTopicCreate, s_small.TagTopicUpdate]):

    def get_tags_of_topic(
        self, db: Session, *, topic_uniq_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[m_small.TagDB]:
        return (
            db.query(m_small.TagDB)
            .filter(m_topic.TopicMetaDB.uniq_id == topic_uniq_id)
            .filter(m_topic.TopicMetaDB.uniq_id == m_small.TagTopicDB.topic_uniq_id)
            .filter(m_small.TagDB.uniq_id == m_small.TagTopicDB.tag_uniq_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_tag_topic = CRUDTagTopic(m_small.TagTopicDB)


class CRUDRecord(CRUDBase[m_small.RecordDB, s_small.RecordCreate, s_small.RecordUpdate]):
    def get_record_by_filename(
        self, db: Session, *, filename: str
    ) -> m_small.RecordDB:
        return (
            db.query(self.model)
            .filter(m_small.RecordDB.filename == filename)
            .first()
        )

    def get_records_of_user_by_uniq_id(
        self, db: Session, *, user_uniq_id: UUID, skip: int = 0, limit: int = 100
    ) -> m_small.RecordDB:
        return (
            db.query(m_small.RecordDB)
            .filter(m_small.RecordDB.owner_uniq_id == user_uniq_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_record = CRUDRecord(m_small.RecordDB)


class CRUDReadText(CRUDBase[m_small.ReadTextDB, s_small.ReadTextCreate, s_small.ReadTextUpdate]):
    def get_rad_texts_of_user_by_uniq_id(
        self, db: Session, *, user_uniq_id: UUID, skip: int = 0, limit: int = 100
    ) -> m_small.ReadTextDB:
        return (
            db.query(m_small.ReadTextDB)
            .filter(m_small.ReadTextDB.owner_uniq_id == user_uniq_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_read_text = CRUDReadText(m_small.ReadTextDB)


class CRUDCommentar(CRUDBase[m_small.CommentarDB, s_small.CommentarCreate, s_small.CommentarUpdate]):
    def get_commentars_of_user_by_uniq_id(
        self, db: Session, *, user_uniq_id: UUID, skip: int = 0, limit: int = 100
    ) -> m_small.RecordDB:
        return (
            db.query(m_small.CommentarDB)
            .filter(m_small.CommentarDB.owner_uniq_id == user_uniq_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_commentar = CRUDCommentar(m_small.CommentarDB)
