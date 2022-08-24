from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.queries import queries_answer
from app.models.m_answer import AnswerMetaDB
from app.schemas.s_answer import AnswerMetaCreate, AnswerMetaUpdate
from sqlalchemy import text
from app.models import m_small, m_question, m_answer, m_topic
from app.schemas import s_small, s_question, s_answer, s_topic


class CRUDAnswer(CRUDBase[AnswerMetaDB, AnswerMetaCreate, AnswerMetaUpdate]):
    def get_meta_by_topic_uniq_id(
        self, db: Session, *, topic_uniq_id: UUID
    ) -> AnswerMetaDB:
        result = (
            db.query(AnswerMetaDB)
            .filter(AnswerMetaDB.topic_uniq_id == topic_uniq_id)
            .first()
        )
        return result


    # @staticmethod
    # def create_answer(
    #         db: Session, *, owner_uniq_id: str, commentar_uniq_id: str, record_uniq_id: str,
    # ) -> m_answer.AnswerDB:
    #     result = db.execute(
    #         text(queries_answer.INSERT_SINGLE),
    #         {
    #             "owner_uniq_id": owner_uniq_id,
    #             "commentar_uniq_id": commentar_uniq_id,
    #             "record_uniq_id": record_uniq_id,
    #         }
    #     )
    #     db.commit()
    #     results_as_dict = result.mappings().all()
    #     answer_db = m_answer.AnswerDB(**results_as_dict[0])
    #     return answer_db

    # @staticmethod
    # def remove_by_uniq_id_s(db: Session, *, uniq_id_s: List[str]) -> int:
    #     """
    #     Delete multiple answers by uniq_id supplied in uniq_id_s.
    #     @param db:
    #     @param uniq_id_s:
    #     @return: number of rows deleted
    #     """
    #     nbr_deleted = db.query(m_answer.AnswerDB).filter(
    #         m_answer.AnswerDB.uniq_id.in_(uniq_id_s)
    #     ).delete()
    #     db.commit()
    #     return nbr_deleted

    # @staticmethod
    # def get_combi_by_topic_uniq_id(
    #      db: Session, *, topic_uniq_id: str
    # ) -> Optional[List[AnswerCombiDB]]:
    #     result = (
    #         db.query(AnswerCombiDB)
    #         .from_statement(text(queries_answer.GET_COMBI_BY_TOPIC_UNIQ_ID))
    #         .params(topic_uniq_id=topic_uniq_id)
    #         .all()
    #     )
    #     return (
    #         result
    #     )

    # @staticmethod
    # def get_combi_by_uniq_id(
    #         db: Session, *, answer_uniq_id: str
    # ) -> Optional[AnswerCombiDB]:
    #     result = (
    #         db.query(AnswerCombiDB)
    #         .from_statement(text(queries_answer.GET_COMBI_BY_UNIQ_ID))
    #         .params(answer_uniq_id=answer_uniq_id)
    #         .one()
    #     )
    #     return (
    #         result
    #     )


crud_answer = CRUDAnswer(AnswerMetaDB)
