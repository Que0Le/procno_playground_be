# from typing import Any, Dict, Optional, Union, List
from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.queries import *
from app.models import m_small, m_question, m_answer, m_topic
from app.schemas import s_small, s_question, s_answer, s_topic
from app.models.m_topic import TopicDB, TopicCombiDB
from app.schemas.topic import TopicCreate, TopicUpdate
from sqlalchemy import text


class CRUDTopic(CRUDBase[TopicDB, TopicCreate, TopicUpdate]):
    # Only create the topic, not the relation with question, tag, record, ...
    @staticmethod
    def create_topic(
            db: Session, *, topic_create: s_topic.TopicCreate
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
        # result = (
        #     db.query(TopicCombiDB)
        #     .from_statement(text(sm))
        #     .params(topic_uniq_id=topic_uniq_id)
        #     .one()
        # )
        result = db.execute(
            text(queries_topic.GET_COMBI_BY_TOPIC_UNIQ_ID),
            {"topic_uniq_id": topic_uniq_id}
        )
        db.commit()
        results_as_dict = result.mappings().all()
        question_db = m_topic.TopicCombiDB(**results_as_dict[0])

        return (
            question_db
        )

    @staticmethod
    def get_combi_by_user_id(
            db: Session, *, owner_uniq_id: str, skip: object = 0, limit: object = 100
    ) -> Optional[List[TopicCombiDB]]:
        result = (
            db.query(m_topic.TopicCombiDB)
            .from_statement(text(queries_topic.GET_COMBI_BY_USER_UNIQ_ID))
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

    @staticmethod
    def remove_by_topic_uniq_id(db: Session, *, topic_uniq_id: str) -> m_topic.TopicQuestionDB:
        obj = db.query(m_topic.TopicQuestionDB).filter(m_topic.TopicQuestionDB.topic_uniq_id == topic_uniq_id).one()
        db.delete(obj)
        db.commit()
        return obj


topic_question = CRUDTopicQuestion(m_topic.TopicQuestionDB)


class CRUDTopicAnswer(CRUDBase[m_topic.TopicAnswerDB, s_topic.TopicAnswerCreate, s_topic.TopicAnswerUpdate]):
    @staticmethod
    def create_topic_answer_relation(
            db: Session, *, topic_uniq_id: str, answer_uniq_id: str
    ) -> m_topic.TopicAnswerDB:
        result = db.execute(
            text(queries_topic_answer.INSERT_SINGLE),
            {"topic_uniq_id": topic_uniq_id, "answer_uniq_id": answer_uniq_id}
        )
        db.commit()
        results_as_dict = result.mappings().all()
        topic_answer_db = m_topic.TopicAnswerDB(**results_as_dict[0])
        return topic_answer_db

    @staticmethod
    def remove_by_topic_uniq_id(db: Session, *, topic_uniq_id: str) -> int:
        """
        Delete multiple topic_answer by topic uniq_id.
        @param db:
        @param topic_uniq_id:
        @return: number of rows deleted
        """
        nbr_deleted = db.query(m_topic.TopicAnswerDB).filter(
            m_topic.TopicAnswerDB.topic_uniq_id == topic_uniq_id
        ).delete()
        db.commit()
        return nbr_deleted

    @staticmethod
    def get_multi_by_topic_uniq_id(
            db: Session, *, topic_uniq_id: str
    ) -> List[m_topic.TopicAnswerDB]:
        return (
            db.query(m_topic.TopicAnswerDB)
            .filter(m_topic.TopicAnswerDB.topic_uniq_id == topic_uniq_id)
            # .offset(skip)
            # .limit(limit)
            .all()
        )


topic_answer = CRUDTopicAnswer(m_topic.TopicAnswerDB)


