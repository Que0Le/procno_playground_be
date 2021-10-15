from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_question import QuestionDB, QuestionCombiDB
from app.schemas.s_question import QuestionBase, QuestionCreate, QuestionUpdate, QuestionInDBBase
from sqlalchemy import text

class CRUDQuestion(CRUDBase[QuestionDB, QuestionCreate, QuestionUpdate]):
    
    def get_combi_by_topic_id(
        self, db: Session, *, id: int, skip=0, limit=100
    ) -> Optional[List[QuestionCombiDB]]:
        sm = """
            SELECT 
                questions.id as q_id,
                questions.created_at as q_created_at,
                questions.updated_at as q_updated_at,
                read_texts.read_text as rt_read_text,
                read_texts.created_at as rt_created_at,
                read_texts.updated_at as rt_updated_at,
                records.filename as rc_filename,
                records.created_at as rc_created_at,
                records.updated_at as rc_updated_at,
                commentars.commentar as c_commentar,
                commentars.created_at as c_created_at,
                commentars.updated_at as c_updated_at
            FROM questions 
            LEFT JOIN read_texts ON questions.text_id =read_texts.id 
            LEFT JOIN records ON questions.record_id =records.id 
            LEFT JOIN commentars ON questions.commentar_id =commentars.id 
            where questions.id = (
                select topics.question_id 
                from topics 
                where topics.id = :topic_id
            )
            """
        result = (
            db.query(QuestionCombiDB)
            .from_statement(text(sm))
            .params(topic_id=id)
            .all()
        )
        return (
            result
        )


question = CRUDQuestion(QuestionDB)
