from typing import Any, List
from fastapi import APIRouter, Depends
from app import models, schemas, crud
from app.api import deps
from sqlalchemy.orm import Session
from datetime import datetime
# from uuid import UUID

router = APIRouter()


@router.post("/own-topics/", status_code=200)
def create_new_own_topic(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.UserDB = Depends(deps.get_current_user),
    topic_create: schemas.s_topic.TopicCreate,
) -> Any:
    topic_create.topic_title = topic_create.topic_title + str(datetime.now())
    topic_create.owner_uniq_id = current_user.uniq_id
    topic_create.owner_username = current_user.username
    topic_create.record_filename = str(datetime.now())  # TODO: record audio

    # Add to topic table
    topic_db = crud.topic.create_topic(db=db, topic_create=topic_create)

    # Add tags and relation with topic
    tag_db_s = []
    tag_topic_db_s = []
    for tag_name in topic_create.tags:
        tag_db = crud.tag.create_tag(db=db, tag_name=tag_name + str(datetime.now()), description="")
        tag_db_s.append(tag_db)
        #
        tag_topic_db = crud.tag_topic.create_tag_topic_relation(
            db=db, topic_uniq_id=topic_db.uniq_id, tag_uniq_id=tag_db.uniq_id
        )
        tag_topic_db_s.append(tag_topic_db)

    # Add record
    record_db = crud.record.create_record(
        db=db,
        filename=topic_create.record_filename, owner_uniq_id=topic_create.owner_uniq_id
    )
    # Add read text
    readtext_db = crud.read_text.create_read_text(
        db=db,
        read_text_from_user=topic_create.readtext, owner_uniq_id=topic_create.owner_uniq_id
    )
    # Add commentar
    commentar_db = crud.commentar.create_commentar(
        db=db,
        commentar_from_user=topic_create.commentar, owner_uniq_id=topic_create.owner_uniq_id
    )

    # Add question and relation with topic
    question_db = crud.question.create_question(
        db=db,
        owner_uniq_id=topic_create.owner_uniq_id, commentar_uniq_id=commentar_db.uniq_id,
        record_uniq_id=record_db.uniq_id, text_uniq_id=readtext_db.uniq_id
    )
    topic_question_db = crud.topic_question.create_topic_question_relation(
        db=db,
        topic_uniq_id=topic_db.uniq_id, question_uniq_id=question_db.uniq_id
    )

    # Now try retrieve the recently added topic:
    topic_db = crud.topic.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=topic_db.uniq_id)
    topic_get = schemas.create_topic_combi_from_db_model(topic_db)

    return {
        "status": "success",
        "topic": topic_get
    }


@router.get("/own-topics/", response_model=List[schemas.TopicOverviewGet], status_code=200)
def get_own_topic_overviews(
    db: Session = Depends(deps.get_db),
    current_user: models.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Get topic overviews created by current user
    """
    topics_db = crud.topic.get_combi_by_user_id(db=db, owner_uniq_id=current_user.uniq_id)
    r = []
    for topic_db in topics_db:
        temp = schemas.create_topic_combi_from_db_model(topic_db)
        if temp:
            r.append(temp)
    return r


@router.get("/uniq_id/{uniq_id}", response_model=schemas.TopicOverviewGet, status_code=200)
def get_topic_overview_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    uniq_id: str
) -> Any:
    """
    Get a topic by its uniq_id
    """
    topic_db = crud.topic.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=uniq_id)
    topic_get = schemas.create_topic_combi_from_db_model(topic_db)
    return topic_get


# @router.post("/test-any/", status_code=200)
# def test_any(
#     db: Session = Depends(deps.get_db)
# ) -> Any:
#     """
#     Test anything.
#     """
#     # r = crud.answer.get_answers_combi_by_topic_id(db=db, id=1, limit=1)
#     r = crud.topic.get_combi_by_topic_id(db=db, id=3, limit=1)
#     # r = crud.question.get_combi_by_topic_id(db=db, id=1, limit=1)
#     return r
    # return {"msg": "Test request sent"}
