from datetime import datetime
from typing import Optional, List
import uuid
import logging

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
        self, db: Session, *, user_uniq_id: str, skip: int = 0, limit: int = 100
    ) -> List[s_small.UserRoleGet]:
        # logging.getLogger(__name__).info("test")
        try:
            result = (
                db.query(
                    m_user.UserDB.uniq_id, m_user.UserDB.username,
                    m_small.RoleDB.uniq_id, m_small.RoleDB.role_name, 
                    m_small.RoleDB.description, m_small.UserRoleDB.created_at
                )
                .filter(m_user.UserDB.uniq_id == user_uniq_id)
                .filter(m_user.UserDB.uniq_id == m_small.UserRoleDB.user_uniq_id)
                .filter(m_small.RoleDB.uniq_id == m_small.UserRoleDB.role_uniq_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            if len(result) > 0:
                return [s_small.UserRoleGet(*r) for r in result]
        except Exception as e:
            # logger.error(type(e))
            # logger.error(e.args)
            # logger.error(e)
            #TODO: logging
            print(e)
            pass

        return []


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
        self, db: Session, *, topic_uniq_id: str, skip: int = 0, limit: int = 100
    ) -> List[s_small.TagTopicGet]:
        # logging.getLogger(__name__).info("test")
        try:
            result = (
                db.query(
                    m_topic.TopicDB.uniq_id, m_topic.TopicDB.title,
                    m_small.TagDB.uniq_id, m_small.TagDB.tag_name, 
                    m_small.TagDB.description, m_small.TagTopicDB.created_at
                )
                .filter(m_topic.TopicDB.uniq_id == topic_uniq_id)
                .filter(m_topic.TopicDB.uniq_id == m_small.TagTopicDB.topic_uniq_id)
                .filter(m_small.TagDB.uniq_id == m_small.TagTopicDB.tag_uniq_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            if len(result) > 0:
                return [s_small.TagTopicGet(*r) for r in result]
        except Exception as e:
            # logger.error(type(e))
            # logger.error(e.args)
            # logger.error(e)
            pass

        return []


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
        self, db: Session, *, user_uniq_id: str, skip: int = 0, limit: int = 100
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
    @staticmethod
    def create_read_text(
            db: Session, *, read_text_from_user: str, owner_uniq_id: str
    ) -> Optional[m_small.ReadTextDB]:
        result = db.execute(
            text(queries_read_text.INSERT_SINGLE),
            {"read_text": read_text_from_user, "owner_uniq_id": owner_uniq_id}
        )
        db.commit()
        results_as_dict = result.mappings().all()
        read_text_db = m_small.ReadTextDB(**results_as_dict[0])
        return read_text_db


crud_read_text = CRUDReadText(m_small.ReadTextDB)


class CRUDCommentar(CRUDBase[m_small.CommentarDB, s_small.CommentarCreate, s_small.CommentarUpdate]):
    @staticmethod
    def create_commentar(
            db: Session, *, commentar_from_user: str, owner_uniq_id: str
    ) -> Optional[m_small.CommentarDB]:
        result = db.execute(
            text(queries_commentar.INSERT_SINGLE),
            {"commentar": commentar_from_user, "owner_uniq_id": owner_uniq_id}
        )
        db.commit()
        results_as_dict = result.mappings().all()
        commentar_db = m_small.CommentarDB(**results_as_dict[0])
        return commentar_db


crud_commentar = CRUDCommentar(m_small.CommentarDB)
