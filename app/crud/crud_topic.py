from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_topic import TopicDB, TopicCombiDB
from app.models.m_answer import AnswerCombiDB
from app.schemas.topic import TopicBase, TopicCreate, TopicUpdate, TopicInDBBase
from sqlalchemy import text

class CRUDTopic(CRUDBase[TopicDB, TopicCreate, TopicUpdate]):
    def get_all_by_topic_title(
        self, db: Session, *, title: str, skip=0, limit=100
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_one_by_topic_title(
        self, db: Session, *, title: str
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)
            .first()
        )

    def get_one_by_topic_id(
        self, db: Session, *, id: int
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.id == id)
            .first()
        )

    def get_combi_by_topic_id(
        self, db: Session, *, id: int, skip=0, limit=100
    ) -> Optional[List[TopicCombiDB]]:
        sm = """
            select 
                topics.id  as t_id,
                topics.title as t_title,
                topics.source_language as t_source_language,
                topics.source_level as t_source_level,
                topics.wish_correct_languages as t_wish_correct_languages,
                topics.created_at t_created_at,
                topics.updated_at t_updated_at,
                --
                temp1_tags.tt_tags,
                --
                temp2_nbr_ans.nbr_answers,
                --
                temp3_question_data.q_created_at,
                temp3_question_data.q_updated_at,
                temp3_question_data.rt_read_text,
                temp3_question_data.rt_created_at,
                temp3_question_data.rt_updated_at,
                temp3_question_data.rc_filename,
                temp3_question_data.rc_created_at,
                temp3_question_data.rc_updated_at,
                temp3_question_data.c_commentar,
                temp3_question_data.c_created_at,
                temp3_question_data.c_updated_at
            from topics
            -- temp table for tags for topic id
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    array_agg(tags.tag_name) as tt_tags
                FROM topics
                INNER JOIN tag_topic
                ON tag_topic.topic_id = topics.id
                INNER JOIN tags
                ON tags.id = tag_topic.tag_id
                where topics.id = :topic_id
                GROUP BY topics.id, topics.title
            ) temp1_tags 
            on temp1_tags.t_id = topics.id
            -- temp table for number of answers
            inner join (	
                SELECT 
                    topics.id as t_id , 
                    count( topic_answers.answer_id ) as nbr_answers
                FROM topics LEFT JOIN topic_answers ON topics.id=topic_answers.topic_id 
                where topics.id = :topic_id
                GROUP BY topics.id
            ) temp2_nbr_ans 
            on temp2_nbr_ans.t_id = topics.id
            -- temp table for question data: text+comment+record file
            inner join (
                SELECT 
                    :topic_id as t_id,
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
            ) temp3_question_data
            on temp3_question_data.t_id = topics.id 
            where topics.id = :topic_id
            """
        result = (
            db.query(TopicCombiDB)
            .from_statement(text(sm))
            .params(topic_id=id, skip=skip, limit=limit)
            .all()
        )
        return (
            result
        )
        
    def get_combi_by_user_id(
        self, db: Session, *, owner_id: int, skip=0, limit=100
    ) -> Optional[List[TopicCombiDB]]:
        sm = """
            -- get topic-combi by owner id
            select 
                topics.uniq_id  as t_uniq_id,
                topics.title as t_title,
                topics.source_language as t_source_language,
                topics.source_level as t_source_level,
                topics.wish_correct_languages as t_wish_correct_languages,
                topics.created_at t_created_at,
                topics.updated_at t_updated_at,
                ----------
                temp1_tags.tt_tags,
                temp1_tags.tt_tag_uuids,
                ----------
                temp2_nbr_ans.nbr_answers,
                ----------
                temp3_question_data.q_uniq_id,
                temp3_question_data.q_created_at,
                temp3_question_data.q_updated_at,
                --
                temp3_question_data.rt_uniq_id,
                temp3_question_data.rt_read_text,
                temp3_question_data.rt_created_at,
                temp3_question_data.rt_updated_at,
                --
                temp3_question_data.rc_uniq_id,
                temp3_question_data.rc_filename,
                temp3_question_data.rc_created_at,
                temp3_question_data.rc_updated_at,
                --
                temp3_question_data.c_uniq_id,
                temp3_question_data.c_commentar,
                temp3_question_data.c_created_at,
                temp3_question_data.c_updated_at
            from topics
            -- temp table for tags for topic id
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    array_agg(tags.tag_name) as tt_tags,
                    array_agg(tags.uniq_id) as tt_tag_uuids
                FROM topics
                INNER JOIN tag_topic
                ON tag_topic.topic_id = topics.id
                INNER JOIN tags
                ON tags.id = tag_topic.tag_id
                GROUP BY topics.id, topics.title
            ) temp1_tags 
            on temp1_tags.t_id = topics.id
            -- temp table for number of answers
            inner join (	
                SELECT 
                    topics.id as t_id , 
                    count( topic_answer.answer_id ) as nbr_answers
                FROM topics LEFT JOIN topic_answer ON topics.id=topic_answer.topic_id 
                GROUP BY topics.id
            ) temp2_nbr_ans 
            on temp2_nbr_ans.t_id = topics.id
            -- temp table for question data: text+comment+record file
            -------------------------------------------------------------------------------------------------
            inner join (
                SELECT 
                    topic_question.topic_id as t_id,
                    questions.uniq_id as q_uniq_id,
                    questions.created_at as q_created_at,
                    questions.updated_at as q_updated_at,
                    read_texts.uniq_id as rt_uniq_id,
                    read_texts.read_text as rt_read_text,
                    read_texts.created_at as rt_created_at,
                    read_texts.updated_at as rt_updated_at,
                    records.uniq_id as rc_uniq_id,
                    records.filename as rc_filename,
                    records.created_at as rc_created_at,
                    records.updated_at as rc_updated_at,
                    commentars.uniq_id as c_uniq_id,
                    commentars.commentar as c_commentar,
                    commentars.created_at as c_created_at,
                    commentars.updated_at as c_updated_at
                FROM questions 
                LEFT JOIN topic_question ON questions.id =topic_question.question_id 
                LEFT JOIN read_texts ON questions.text_id =read_texts.id 
                LEFT JOIN records ON questions.record_id =records.id 
                LEFT JOIN commentars ON questions.commentar_id =commentars.id 
                group by 
                    questions.uniq_id, questions.id, topic_question.topic_id, questions.uniq_id,
                    read_texts.uniq_id, read_texts.read_text, read_texts.created_at, read_texts.updated_at,
                    records.uniq_id, records.filename, records.created_at, records.updated_at,
                    commentars.uniq_id, commentars.commentar, commentars.created_at, commentars.updated_at
            ) temp3_question_data
            on temp3_question_data.t_id = topics.id 
            where topics.id in (
                select id from topics where owner_id = :owner_id
            )
            ORDER by t_created_at DESC 
            OFFSET :skip
            LIMIT :limit
            """
        result = (
            db.query(TopicCombiDB)
            .from_statement(text(sm))
            .params(owner_id=owner_id, skip=skip, limit=limit)
            .all()
        )
        return (
            result
        )


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


topic = CRUDTopic(TopicDB)
