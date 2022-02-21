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


# TODO: get own answers (from public topics)
@router.get("/own-answers/")
def get_own_answers(
    db: Session = Depends(deps.get_db),
    current_user: models.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Get topic overviews created by current user
    """
    return {}


@router.get(
    "/for-topic/{topic_uniq_id}",
    response_model=List[schemas.s_answer.AnswerOverviewGet],
    status_code=200
)
def get_topic_overview_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    topic_uniq_id: str
) -> Any:
    """
    Get a topic by its uniq_id
    """
    answers_db = crud.answer.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=topic_uniq_id)
    answers_get = []
    for answer_db in answers_db:
        temp = schemas.s_answer.create_answer_combi_from_db_model(answer_db)
        if temp:
            answers_get.append(temp)
    return answers_get
