from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
# from app.models.m_question import QuestionDB, QuestionCombiDB
# from app.schemas.s_question import QuestionBase, QuestionCreate, QuestionUpdate
from sqlalchemy import text
from app.db.queries import *
from app.schemas import s_small, s_topic, s_question
from app.models import m_small, m_topic, m_answer, m_question


class CRUDQuestion(CRUDBase[m_question.QuestionDB, s_question.QuestionCreate, s_question.QuestionUpdate]):

    @staticmethod
    def create_question(
            db: Session, *,
            owner_uniq_id: str, commentar_uniq_id: str,
            record_uniq_id: str, text_uniq_id: str
    ) -> Optional[m_question.QuestionDB]:
        result = db.execute(
            text(queries_question.INSERT_SINGLE),
            {
                "owner_uniq_id": owner_uniq_id, "commentar_uniq_id": commentar_uniq_id,
                "record_uniq_id": record_uniq_id, "text_uniq_id": text_uniq_id
            }
        )
        db.commit()
        results_as_dict = result.mappings().all()
        question_db = m_question.QuestionDB(**results_as_dict[0])
        return question_db

    @staticmethod
    def get_question_by_topic_uniq_id(
            db: Session, *,
            topic_uniq_id: str
    ) -> Optional[m_question.QuestionDB]:
        result = (
            db.query(m_question.QuestionDB)
            .from_statement(text(queries_question.GET_QUESTION_BY_TOPIC_UNIQ_ID))
            .params(topic_uniq_id=topic_uniq_id)
            .all()
        )
        return result


question = CRUDQuestion(m_question.QuestionDB)


# class CRUDTopicQuestion(CRUDBase[m_topic.TopicQuestionDB, s_topic.TopicQuestionCreate, s_topic.TopicQuestionUpdate]):
#     @staticmethod
#     def create_topic_question(
#             db: Session, *,
#             owner_uniq_id: str, question_uniq_id: str
#     ) -> Optional[m_topic.TopicQuestionDB]:
#         result = db.execute(
#             text(queries_topic_question.INSERT_SINGLE),
#             {
#                 "owner_uniq_id": owner_uniq_id, "question_uniq_id": question_uniq_id,
#             }
#         )
#         db.commit()
#         results_as_dict = result.mappings().all()
#         topic_question_db = m_topic.TopicQuestionDB(**results_as_dict[0])
#         return topic_question_db
#
#     @staticmethod
#     def remove_by_topic_uniq_id(db: Session, *, topic_uniq_id: str) -> m_topic.TopicQuestionDB:
#         obj = db.query(m_topic.TopicQuestionDB).get(topic_uniq_id)
#         db.delete(obj)
#         db.commit()
#         return obj
#
#
# topic_question = CRUDTopicQuestion(m_topic.TopicQuestionDB)
