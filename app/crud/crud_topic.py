# from typing import Any, Dict, Optional, Union, List
from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.queries import *
from app.models import m_small, m_question, m_answer, m_topic
from app.schemas import s_small, s_question, s_answer, s_topic
from app.models.m_topic import TopicDB, TopicCombiDB
# from app.models.m_answer import AnswerCombiDB
from app.schemas.topic import TopicCreate, TopicUpdate
from sqlalchemy import text
from sqlalchemy import text


class CRUDTopic(CRUDBase[TopicDB, TopicCreate, TopicUpdate]):
    # Only create the topic, not the relation with question, tag, record, ...
    @staticmethod
    def create_topic(
            db: Session, *,  topic_create: s_topic.TopicCreate
    ) -> m_topic.TopicDB:
        result = db.execute(
            text(queries_topic.INSERT_SINGLE),
            {
                "title": topic_create.topic_title,
                "source_language": topic_create.source_language,
                "source_level": topic_create.source_level,
                "wish_correct_languages": topic_create.wish_correct_languages,
                "owner_uniq_id": topic_create.owner_uniq_id,
            }
        )
        db.commit()
        results_as_dict = result.mappings().all()
        topic_db = m_topic.TopicDB(**results_as_dict[0])
        return topic_db

    @staticmethod
    def get_all_by_topic_title(
            db: Session, *, title: str, skip=0, limit=100
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_one_by_topic_title(
            db: Session, *, title: str
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.title == title)
            .first()
        )

    @staticmethod
    def get_one_by_topic_uniq_id(
            db: Session, *, uniq_id: str
    ) -> Optional[TopicDB]:
        return (
            db.query(TopicDB)
            .filter(TopicDB.uniq_id == uniq_id)
            .first()
        )

    @staticmethod
    def get_combi_by_topic_uniq_id(
            db: Session, *, topic_uniq_id: str
    ) -> Optional[TopicCombiDB]:
        sm = """
            select 
                -- topics.id  as t_id,
                topics.uniq_id  as t_uniq_id,
                topics.title as t_title,
                topics.source_language as t_source_language,
                topics.source_level as t_source_level,
                topics.wish_correct_languages as t_wish_correct_languages,
                topics.created_at t_created_at,
                topics.updated_at t_updated_at,
                ----------
                temp_owner.u_uniq_id,
                temp_owner.u_username,
                ----------
                temp_nbr_ans.nbr_answers,
                ----------
                temp_tags.tt_tags,
                temp_tags.tt_tag_uuids,
                ----------
                temp_question_data.q_uniq_id,
                temp_question_data.q_created_at,
                temp_question_data.q_updated_at,
                --
                temp_question_data.rt_uniq_id,
                temp_question_data.rt_read_text,
                temp_question_data.rt_created_at,
                temp_question_data.rt_updated_at,
                --
                temp_question_data.rc_uniq_id,
                temp_question_data.rc_filename,
                temp_question_data.rc_created_at,
                temp_question_data.rc_updated_at,
                --
                temp_question_data.c_uniq_id,
                temp_question_data.c_commentar,
                temp_question_data.c_created_at,
                temp_question_data.c_updated_at
            from topics
            -- temp table for tags for topic id
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    topics.uniq_id as t_uniq_id, 
                    array_agg(tags.tag_name) as tt_tags,
                    array_agg(tags.uniq_id) as tt_tag_uuids
                FROM topics
                INNER JOIN tag_topic
                ON tag_topic.topic_uniq_id = topics.uniq_id
                INNER JOIN tags
                ON tags.uniq_id = tag_topic.tag_uniq_id
                GROUP BY topics.uniq_id, topics.title
            ) temp_tags 
            on temp_tags.t_uniq_id = topics.uniq_id
            -- temp table for number of answers
            inner join (	
                SELECT 
                    topics.uniq_id as t_uniq_id , 
                    count( topic_answer.answer_uniq_id ) as nbr_answers
                FROM topics LEFT JOIN topic_answer ON topics.uniq_id=topic_answer.topic_uniq_id 
                GROUP BY topics.uniq_id
            ) temp_nbr_ans 
            on temp_nbr_ans.t_uniq_id = topics.uniq_id
            -- temp table for question data: text+comment+record file
            -------------------------------------------------------------------------------------------------
            inner join (
                SELECT 
                    topic_question.topic_uniq_id as t_uniq_id,
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
                LEFT JOIN topic_question ON questions.uniq_id =topic_question.question_uniq_id 
                LEFT JOIN read_texts ON questions.text_uniq_id =read_texts.uniq_id 
                LEFT JOIN records ON questions.record_uniq_id =records.uniq_id 
                LEFT JOIN commentars ON questions.commentar_uniq_id =commentars.uniq_id 
                group by 
                    questions.uniq_id, questions.id, topic_question.topic_uniq_id, questions.uniq_id,
                    read_texts.uniq_id, read_texts.read_text, read_texts.created_at, read_texts.updated_at,
                    records.uniq_id, records.filename, records.created_at, records.updated_at,
                    commentars.uniq_id, commentars.commentar, commentars.created_at, commentars.updated_at
            ) temp_question_data
            on temp_question_data.t_uniq_id = topics.uniq_id 
            -- temp table for user infor: uuid and username
            -------------------------------------------------------------------------------------------------
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    topics.uniq_id as t_uniq_id, 
                    users.username as u_username,
                    users.uniq_id as u_uniq_id
                FROM topics
                INNER JOIN users
                ON topics.owner_uniq_id = users.uniq_id
                GROUP BY topics.id, topics.uniq_id, users.username, users.uniq_id
            ) temp_owner 
            on temp_owner.t_uniq_id = topics.uniq_id
            -------------------------------------------------------------------------------------------------
            where topics.uniq_id = :topic_uniq_id
            """
        result = (
            db.query(TopicCombiDB)
            .from_statement(text(sm))
            .params(topic_uniq_id=topic_uniq_id)
            .one()
        )
        return result

    @staticmethod
    def get_combi_by_user_id(
            db: Session, *, owner_uniq_id: str, skip: object = 0, limit: object = 100
    ) -> Optional[List[TopicCombiDB]]:
        sm = """
            -- get topic-combi by owner id
            select 
                topics.id  as t_id,
                topics.uniq_id  as t_uniq_id,
                topics.title as t_title,
                topics.source_language as t_source_language,
                topics.source_level as t_source_level,
                topics.wish_correct_languages as t_wish_correct_languages,
                topics.created_at t_created_at,
                topics.updated_at t_updated_at,
                ----------
                temp_owner.u_uniq_id,
                temp_owner.u_username,
                ----------
                temp_nbr_ans.nbr_answers,
                ----------
                temp_tags.tt_tags,
                temp_tags.tt_tag_uuids,
                ----------
                temp_question_data.q_uniq_id,
                temp_question_data.q_created_at,
                temp_question_data.q_updated_at,
                --
                temp_question_data.rt_uniq_id,
                temp_question_data.rt_read_text,
                temp_question_data.rt_created_at,
                temp_question_data.rt_updated_at,
                --
                temp_question_data.rc_uniq_id,
                temp_question_data.rc_filename,
                temp_question_data.rc_created_at,
                temp_question_data.rc_updated_at,
                --
                temp_question_data.c_uniq_id,
                temp_question_data.c_commentar,
                temp_question_data.c_created_at,
                temp_question_data.c_updated_at
            from topics
            -- temp table for tags for topic id
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    topics.uniq_id as t_uniq_id, 
                    array_agg(tags.tag_name) as tt_tags,
                    array_agg(tags.uniq_id) as tt_tag_uuids
                FROM topics
                INNER JOIN tag_topic
                ON tag_topic.topic_uniq_id = topics.uniq_id
                INNER JOIN tags
                ON tags.uniq_id = tag_topic.tag_uniq_id
                GROUP BY topics.uniq_id, topics.title
            ) temp_tags 
            on temp_tags.t_uniq_id = topics.uniq_id
            -- temp table for number of answers
            inner join (	
                SELECT 
                    topics.uniq_id as t_uniq_id , 
                    count( topic_answer.answer_uniq_id ) as nbr_answers
                FROM topics LEFT JOIN topic_answer ON topics.uniq_id=topic_answer.topic_uniq_id 
                GROUP BY topics.uniq_id
            ) temp_nbr_ans 
            on temp_nbr_ans.t_uniq_id = topics.uniq_id
            -- temp table for question data: text+comment+record file
            -------------------------------------------------------------------------------------------------
            inner join (
                SELECT 
                    topic_question.topic_uniq_id as t_uniq_id,
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
                LEFT JOIN topic_question ON questions.uniq_id =topic_question.question_uniq_id 
                LEFT JOIN read_texts ON questions.text_uniq_id =read_texts.uniq_id 
                LEFT JOIN records ON questions.record_uniq_id =records.uniq_id 
                LEFT JOIN commentars ON questions.commentar_uniq_id =commentars.uniq_id 
                group by 
                    questions.uniq_id, questions.id, topic_question.topic_uniq_id, questions.uniq_id,
                    read_texts.uniq_id, read_texts.read_text, read_texts.created_at, read_texts.updated_at,
                    records.uniq_id, records.filename, records.created_at, records.updated_at,
                    commentars.uniq_id, commentars.commentar, commentars.created_at, commentars.updated_at
            ) temp_question_data
            on temp_question_data.t_uniq_id = topics.uniq_id 
            -- temp table for user infor: uuid and username
            -------------------------------------------------------------------------------------------------
            inner join (	
                SELECT 
                    topics.id as t_id, 
                    topics.uniq_id as t_uniq_id, 
                    users.username as u_username,
                    users.uniq_id as u_uniq_id
                FROM topics
                INNER JOIN users
                ON topics.owner_uniq_id = users.uniq_id
                GROUP BY topics.id, topics.uniq_id, users.username, users.uniq_id
            ) temp_owner 
            on temp_owner.t_uniq_id = topics.uniq_id
            -------------------------------------------------------------------------------------------------
            where topics.uniq_id in (
                select uniq_id from topics where owner_uniq_id = :owner_uniq_id
            )
            ORDER by t_created_at DESC 
            OFFSET :skip
            LIMIT :limit
            """
        result = (
            db.query(TopicCombiDB)
            .from_statement(text(sm))
            .params(owner_uniq_id=owner_uniq_id, skip=skip, limit=limit)
            .all()
        )
        return (
            result
        )

    @staticmethod
    def get_topic_by_uniq_id(
            db: Session, *, uniq_id: str
    ) -> Optional[TopicDB]:
        sm = """
            -- get topic-combi by owner id
            SELECT * FROM public.topics WHERE uniq_id = :uniq_id
            """
        result = (
            db.query(TopicDB)
            .from_statement(text(sm))
            .params(uniq_id=uniq_id)
            .one()
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


class CRUDTopicQuestion(CRUDBase[m_topic.TopicQuestionDB, s_small.TagTopicCreate, s_small.TagTopicUpdate]):
    @staticmethod
    def create_topic_question_relation(
            db: Session, *, topic_uniq_id: str, question_uniq_id: str
    ) -> m_topic.TopicQuestionDB:
        result = db.execute(
            text(queries_topic_question.INSERT_SINGLE),
            {"topic_uniq_id": topic_uniq_id, "question_uniq_id": question_uniq_id}
        )
        db.commit()
        results_as_dict = result.mappings().all()
        topic_question_db = m_topic.TopicQuestionDB(**results_as_dict[0])
        return topic_question_db


topic_question = CRUDTopicQuestion(m_topic.TopicQuestionDB)

