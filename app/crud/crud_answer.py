from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_answer import AnswerDB, AnswerCombiDB
from app.schemas.s_answer import AnswerCreate, AnswerUpdate
from sqlalchemy import text


class CRUDAnswer(CRUDBase[AnswerDB, AnswerCreate, AnswerUpdate]):

    @staticmethod
    def get_combi_by_topic_uniq_id(
         db: Session, *, topic_uniq_id: str
    ) -> Optional[List[AnswerCombiDB]]:
        sm = """
            select 
                answers.uniq_id as ans_uniq_id,
                answers.created_at as ans_created_at,
                answers.updated_at as ans_updated_at,
                --
                users.uniq_id as u_uniq_id, 
                users.username as u_username,  
                users.created_at as u_created_at,  
                --
                commentars.uniq_id as c_uniq_id, 
                commentars.commentar as c_commentar,  
                commentars.created_at as c_created_at,  
                commentars.updated_at as c_updated_at,  
                --
                records.uniq_id as rc_uniq_id, 
                records.filename as rc_filename,  
                records.created_at as rc_created_at, 
                records.updated_at as rc_updated_at
            
            from answers
            inner join commentars on answers.commentar_uniq_id = commentars.uniq_id 
            inner join records on answers.record_uniq_id = records.uniq_id 
            inner join users on answers.owner_uniq_id = users.uniq_id 
            
            where answers.uniq_id in (
                select answer_uniq_id 
                from topic_answer tq 
                where topic_uniq_id = :topic_uniq_id
            )
            """
        result = (
            db.query(AnswerCombiDB)
            .from_statement(text(sm))
            .params(topic_uniq_id=topic_uniq_id)
            .all()
        )
        return (
            result
        )


answer = CRUDAnswer(AnswerDB)
