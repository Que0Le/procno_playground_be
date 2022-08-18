import os
from typing import Any, List
from datetime import datetime
import random
import string

from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_answer, crud_small, crud_topic

from app.models import *
from app.models import m_user
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_answer


router = APIRouter()


# TODO: get own answers (from public topics)
@router.get("/own-answers/")
def get_own_answers(
    db: Session = Depends(deps.get_db),
    current_user: m_user.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Get topic overviews created by current user
    """
    return {}


@router.post("/own-answers/", status_code=status.HTTP_201_CREATED)
async def create_new_answer(
        *,
        db: Session = Depends(deps.get_db),
        current_user: m_user.UserDB = Depends(deps.get_current_user),
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
    record_db = crud_small.crud_record.create_record(
        db=db,
        filename=filename, owner_uniq_id=current_user.uniq_id
    )
    # Add commentar
    commentar_db = crud_small.crud_commentar.create_commentar(
        db=db,
        commentar_from_user=commentar, owner_uniq_id=current_user.uniq_id
    )

    # Add question and relation with topic
    answer_db = crud_answer.crud_answer.create_answer(
        db=db,
        owner_uniq_id=current_user.uniq_id, commentar_uniq_id=commentar_db.uniq_id,
        record_uniq_id=record_db.uniq_id
    )
    topic_answer_db = crud_topic.crud_topic_answer.create_topic_answer_relation(
        db=db,
        topic_uniq_id=topic_uniq_id, answer_uniq_id=answer_db.uniq_id
    )

    """ Write file """
    with open(f"./data/records/{filename}", "wb+") as f:
        f.write(file.file.read())

    """ Now try retrieve the combi for recently added answer """
    answer_combi_db = crud_answer.crud_answer.get_combi_by_uniq_id(db=db, answer_uniq_id=answer_db.uniq_id)

    return {
        "status": "success",
        "answer_combi": answer_combi_db
    }


@router.delete("/own-answers/{uniq_id}", status_code=status.HTTP_200_OK)
async def delete_own_answer_by_uniq_id(
        *,
        db: Session = Depends(deps.get_db),
        current_user: m_user.UserDB = Depends(deps.get_current_user),
        uniq_id: str,
) -> Any:

    # Get the combi from DB first
    answer_combi_db = crud_answer.crud_answer.get_combi_by_uniq_id(
        db=db, answer_uniq_id=uniq_id
    )
    if not answer_combi_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found!"
        )
    if answer_combi_db.u_uniq_id != current_user.uniq_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not own answer!"
        )
    # Stupid db cursor: answer_combi_db will be invalid when
    # next expression that requires cursor gets executed.
    # Solution: create copies of data.
    answer_combi = s_answer.create_answer_combi_from_db_model(answer_combi_db)

    # Remove from topic_answer
    nbr_topic_answer_deleted = crud_topic.crud_topic_answer.remove_by_answer_uniq_id(
        db=db, answer_uniq_id=uniq_id
    )
    # Remove from answers
    nbr_answers_deleted = crud_answer.crud_answer.remove_by_uniq_id_s(
        db=db, uniq_id_s=[uniq_id]
    )
    # Remove from commentars
    deleted_commentar = crud_small.crud_commentar.remove(
        db=db, uniq_id=answer_combi.commentar_uniq_id
    )
    # Remove from records
    record_db = crud_small.crud_record.remove(db=db, uniq_id=answer_combi.record_uniq_id)
    if os.path.isfile("./data/records/" + record_db.filename):
        os.remove("./data/records/" + record_db.filename)

    return {
        "status": "success",
        "answer_combi": answer_combi
    }


@router.get(
    "/for-topic/{topic_uniq_id}",
    response_model=List[s_answer.AnswerOverviewGet],
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
    answers_db = crud_answer.crud_answer.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=topic_uniq_id)
    answers_get = []
    for answer_db in answers_db:
        temp = s_answer.create_answer_combi_from_db_model(answer_db)
        if temp:
            answers_get.append(temp)
    return answers_get
