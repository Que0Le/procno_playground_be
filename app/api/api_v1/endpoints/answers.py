from genericpath import isfile
import os
from typing import Any, List, Optional
from datetime import datetime
import random
import string
from uuid import UUID

from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import utilities
from app.crud import crud_small
from app.crud.crud_answer import crud_answer
from app.crud.crud_topic import crud_topic
from app.crud.crud_small import crud_commentar, crud_record
from app.models import m_user
from app.api import deps
from app.core.config import settings
from app.schemas import s_answer, s_small
from app.services import file_helpers
from app.utilities import utils, strings, files_and_dir


router = APIRouter()


""" ANSWERS """


@router.get("/meta", response_model=List[s_answer.AnswerMetaGet])
def get_all_answer_metas(
    db: Session = Depends(deps.get_db),
) -> Any:
    answer_meta_db = crud_answer.get_multi(db=db)
    return answer_meta_db


@router.post("/meta", response_model=s_answer.AnswerMetaGet)
def create_answer_meta(
    *,
    db: Session = Depends(deps.get_db),
    answer_in: s_answer.AnswerMetaCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    answer_meta_db = crud_answer.get_meta_by_topic_uniq_id(
        db=db, topic_uniq_id=answer_in.topic_uniq_id
    )
    if answer_meta_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Answer existed for topic uniq id: {answer_in.topic_uniq_id}"
        )
    answer_meta_db = crud_answer.create(db=db, obj_in=answer_in)
    return answer_meta_db


@router.get("/combine/{answer_uniq_id}", response_model=s_answer.AnswerCombineGet)
def get_answer_combine_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    answer_uniq_id: UUID,
) -> Any:
    # Answer meta
    answer_meta_db = crud_answer.get(db=db, uniq_id=answer_uniq_id)
    if not answer_meta_db:
        raise HTTPException(status_code=404, detail=f"Answer not found: {answer_uniq_id}")
    # Record
    record_db = crud_record.get(db=db, uniq_id=answer_meta_db.record_uniq_id)
    if not record_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Record not found: {answer_meta_db.record_uniq_id} for answer {answer_uniq_id}")
    # Commentar
    commentar_db = crud_commentar.get(db=db, uniq_id=answer_meta_db.commentar_uniq_id)
    if not commentar_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Record not found: {answer_meta_db.commentar_uniq_id} for answer {answer_uniq_id}")
    
    return s_answer.AnswerCombineGet(
        commentar=commentar_db,
        answer=answer_meta_db,
        record=record_db
    )


@router.post("/combine", response_model=s_answer.AnswerCombineGet)
def create_answer_combine(
    *,
    db: Session = Depends(deps.get_db),
    owner_uniq_id: UUID = Form(...),
    topic_uniq_id: UUID = Form(...),
    file: UploadFile = File(...), file_extension: str = Form(...),
    commentar: str = Form(...),
) -> Any:
    # Check existing answer for topic
    answer_meta_db = crud_answer.get_meta_by_topic_uniq_id(
        db=db, topic_uniq_id=topic_uniq_id
    )
    if answer_meta_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Answer existed for topic uniq id: {topic_uniq_id}"
        )
    # Create record
    filename = file_helpers.write_record_file_to_folder(db=db, file=file, file_extension=file_extension)
    if filename == "":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Fail create filename"
        )
    record_db = crud_small.crud_record.create(
        db=db, obj_in=s_small.RecordCreate(filename=filename, owner_uniq_id=owner_uniq_id)
    )
    # Create commentar
    commentar_db = crud_small.crud_commentar.create(
        db=db, obj_in=s_small.CommentarCreate(owner_uniq_id=owner_uniq_id, commentar=commentar)
    )
    # Answer meta
    answer_meta_db = crud_answer.create(
        db=db, obj_in=s_answer.AnswerMetaCreate(
            topic_uniq_id=topic_uniq_id, owner_uniq_id=owner_uniq_id,
            commentar_uniq_id=commentar_db.uniq_id,
            record_uniq_id=record_db.uniq_id,
        )
    )
    return s_answer.AnswerCombineGet(
        answer=answer_meta_db, commentar=commentar_db, record=record_db
    )



""" 
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

    # Add answer and relation with topic
    answer_db = crud_answer.crud_answer.create_answer(
        db=db,
        owner_uniq_id=current_user.uniq_id, commentar_uniq_id=commentar_db.uniq_id,
        record_uniq_id=record_db.uniq_id
    )
    topic_answer_db = crud_topic.crud_topic_answer.create_topic_answer_relation(
        db=db,
        topic_uniq_id=topic_uniq_id, answer_uniq_id=answer_db.uniq_id
    )

    with open(f"./data/records/{filename}", "wb+") as f:
        f.write(file.file.read())

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

    answers_db = crud_answer.crud_answer.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=topic_uniq_id)
    answers_get = []
    for answer_db in answers_db:
        temp = s_answer.create_answer_combi_from_db_model(answer_db)
        if temp:
            answers_get.append(temp)
    return answers_get
"""