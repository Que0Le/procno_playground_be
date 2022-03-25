from typing import Any, List

from fastapi import APIRouter, Depends, status, Form, UploadFile, File
# from pydantic.networks import EmailStr
import random
import string
from app import models, schemas, crud
from app.api import deps
# from app.core.celery_app import celery_app
# from app.schemas.s_topic import TopicOverviewGet
# from app.utils import send_test_email
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
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


@router.post("/own-answers/", status_code=status.HTTP_201_CREATED)
async def create_new_answer(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.UserDB = Depends(deps.get_current_user),
        file: UploadFile = File(...), topic_uniq_id: str = Form(...),
        commentar: str = Form(...),
) -> Any:

    # File sanitize
    # if file.content_type.split("/")[-1] != "webm":
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="File must have content_type audio/webm or video/webm!"
    #     )
    # Generate random file name. TODO: check for duplicated filename in dir!
    filename = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.digits)
        for _ in range(settings.RECORD_FILENAME_LENGTH)
    ) + '.webm'

    """ Write new answer to DB """

    # Add record
    record_db = crud.record.create_record(
        db=db,
        filename=filename, owner_uniq_id=current_user.uniq_id
    )
    # Add commentar
    commentar_db = crud.commentar.create_commentar(
        db=db,
        commentar_from_user=commentar, owner_uniq_id=current_user.uniq_id
    )

    # Add question and relation with topic
    answer_db = crud.answer.create_answer(
        db=db,
        owner_uniq_id=current_user.uniq_id, commentar_uniq_id=commentar_db.uniq_id,
        record_uniq_id=record_db.uniq_id
    )
    topic_answer_db = crud.topic_answer.create_topic_answer_relation(
        db=db,
        topic_uniq_id=topic_uniq_id, answer_uniq_id=answer_db.uniq_id
    )

    """ Write file """
    with open(f"./data/records/{filename}", "wb+") as f:
        f.write(file.file.read())

    """ Now try retrieve the combi for recently added answer """
    answer_combi_db = crud.answer.get_combi_by_uniq_id(db=db, answer_uniq_id=answer_db.uniq_id)

    return {
        "status": "success",
        "answer_combi": answer_combi_db
    }


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
