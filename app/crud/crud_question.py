from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text

from fastapi import Depends

from app.crud.base import CRUDBase
from app.db.queries import *
from app.schemas.s_question import QuestionMetaUpdate, QuestionMetaCreate
from app.models.m_question import QuestionMetaDB
from app.api import deps


class CRUDQuestion(CRUDBase[QuestionMetaDB, QuestionMetaCreate, QuestionMetaUpdate]):
    def get_meta_by_topic_uniq_id(
        self, db: Session, *, topic_uniq_id: UUID
    ) -> QuestionMetaDB:
        result = (
            db.query(QuestionMetaDB)
            .filter(QuestionMetaDB.topic_uniq_id == topic_uniq_id)
            .first()
        )
        return result


crud_question = CRUDQuestion(QuestionMetaDB)
