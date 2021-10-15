from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_answer import AnswerDB, AnswerCombiDB
from app.schemas.s_answer import AnswerBase, AnswerCreate, AnswerUpdate, AnswerInDBBase
from sqlalchemy import text

class CRUDAnswer(CRUDBase[AnswerDB, AnswerCreate, AnswerUpdate]):
    
    def get_answers_combi_by_topic_id(
        self, db: Session, *, id: int, skip=0, limit=100
    ) -> Optional[List[AnswerCombiDB]]:
        sm = """
            SELECT 
                answers.id as a_id,
                answers.created_at as a_created_at,
                answers.updated_at as a_updated_at,
                records.filename as rc_filename,
                records.created_at as rc_created_at,
                records.updated_at as rc_updated_at,
                commentars.commentar as c_commentar,
                commentars.created_at as c_created_at,
                commentars.updated_at as c_updated_at
            FROM answers 
            LEFT JOIN records ON answers.record_id =records.id 
            LEFT JOIN commentars ON answers.commentar_id =commentars.id 
            where answers.id in (
                select 	topic_answers.answer_id 
                from topic_answers 
                where topic_answers.topic_id = :topic_id
            )
            ORDER by a_created_at
            OFFSET :skip
            LIMIT :limit
            """
        result = (
            db.query(AnswerCombiDB)
            .from_statement(text(sm))
            .params(topic_id=id, skip=skip, limit=limit)
            .all()
        )
        return (
            result
        )


answer = CRUDAnswer(AnswerDB)
