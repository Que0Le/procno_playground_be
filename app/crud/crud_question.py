from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
# from app.models.m_question import QuestionDB, QuestionCombiDB
# from app.schemas.s_question import QuestionBase, QuestionCreate, QuestionUpdate
from sqlalchemy import text
from app.db.queries import *
from app.schemas import s_small, s_topic, s_question
from app.models import m_small, m_topic, m_answer, m_question


class CRUDQuestionMeta(
    CRUDBase[m_question.QuestionMetaDB, s_question.QuestionMetaCreate, s_question.QuestionMetaUpdate]
):
    
    def get_meta_by_topic_uniq_id(
        db: Session, *,
        topic_uniq_id: UUID
    ) -> m_question.QuestionMetaDB:
        result = (
            db.query(m_question.QuestionMetaDB)
            .filter(m_question.QuestionMetaDB.topic_uniq_id == topic_uniq_id)
            .first()
        )
        return result

    # @staticmethod
    # def create_question(
    #         db: Session, *,
    #         owner_uniq_id: str, commentar_uniq_id: str,
    #         record_uniq_id: str, text_uniq_id: str
    # ) -> Optional[m_question.QuestionDB]:
    #     result = db.execute(
    #         text(queries_question.INSERT_SINGLE),
    #         {
    #             "owner_uniq_id": owner_uniq_id, "commentar_uniq_id": commentar_uniq_id,
    #             "record_uniq_id": record_uniq_id, "text_uniq_id": text_uniq_id
    #         }
    #     )
    #     db.commit()
    #     results_as_dict = result.mappings().all()
    #     question_db = m_question.QuestionDB(**results_as_dict[0])
    #     return question_db

    # @staticmethod
    # def get_question_by_topic_uniq_id(
    #         db: Session, *,
    #         topic_uniq_id: str
    # ) -> Optional[m_question.QuestionDB]:
    #     result = (
    #         db.query(m_question.QuestionDB)
    #         .from_statement(text(queries_question.GET_QUESTION_BY_TOPIC_UNIQ_ID))
    #         .params(topic_uniq_id=topic_uniq_id)
    #         .all()
    #     )
    #     return result


crud_question = CRUDQuestionMeta(m_question.QuestionMetaDB)
