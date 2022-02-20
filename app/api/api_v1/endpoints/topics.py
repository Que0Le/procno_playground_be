from typing import Any, List

from fastapi import APIRouter, Depends
# from pydantic.networks import EmailStr

from app import models, schemas, crud
from app.api import deps
# from app.core.celery_app import celery_app
# from app.schemas.s_topic import TopicOverviewGet
# from app.utils import send_test_email
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.s_topic import TopicGet
from uuid import UUID

router = APIRouter()


@router.get("/own-topics/", response_model=List[schemas.TopicOverviewGet], status_code=200)
def get_own_topic_overviews(
    db: Session = Depends(deps.get_db),
    current_user: models.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Get topic overviews created by current user
    """
    topics = crud.topic.get_combi_by_user_id(db=db, owner_uniq_id=current_user.uniq_id)
    r = []
    for topic in topics:
        temp = schemas.create_topic_combo_from_db_model(topic)
        if temp:
            r.append(temp)
    return r


@router.get("/uniq_id/{uniq_id}", status_code=200)
def get_topic_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    uniq_id: str
) -> Any:
    """
    Get a topic by its uniq_id
    """
    topic_db = crud.topic.get_topic_by_uniq_id(db=db, uniq_id=uniq_id)
    topic_get = TopicGet(**topic_db.__dict__)
    return {topic_get}


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
