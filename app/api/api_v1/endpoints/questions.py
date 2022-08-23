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
from app.crud.crud_question import crud_question
from app.crud.crud_topic import crud_topic
from app.crud.crud_small import crud_commentar, crud_record, crud_read_text
from app.models import m_user
from app.api import deps
from app.core.config import settings
from app.schemas import s_question, s_small
from app.services import file_helpers
from app.utilities import utils, strings, files_and_dir


router = APIRouter()


""" QUESTIONS """


@router.get("/meta", response_model=List[s_question.QuestionMetaGet])
def get_all_question_metas(
    db: Session = Depends(deps.get_db),
) -> Any:
    question_meta_db = crud_question.get_multi(db=db)
    return question_meta_db


@router.post("/meta", response_model=s_question.QuestionMetaGet)
def create_question_meta(
    *,
    db: Session = Depends(deps.get_db),
    question_in: s_question.QuestionMetaCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    question_meta_db = crud_question.get_meta_by_topic_uniq_id(
        db=db, topic_uniq_id=question_in.topic_uniq_id
    )
    if question_meta_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Question existed for topic uniq id: {question_in.topic_uniq_id}"
        )
    question_meta_db = crud_question.create(db=db, obj_in=question_in)
    return question_meta_db


@router.get("/combine/{question_uniq_id}", response_model=s_question.QuestionCombineGet)
def get_question_combine_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    question_uniq_id: UUID,
) -> Any:
    # Question meta
    question_meta_db = crud_question.get(db=db, uniq_id=question_uniq_id)
    if not question_meta_db:
        raise HTTPException(status_code=404, detail=f"Question not found: {question_uniq_id}")
    # Read text
    read_text_db = crud_read_text.get(db=db, uniq_id=question_meta_db.read_text_uniq_id)
    if not read_text_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Read text not found: {question_meta_db.read_text_uniq_id} for question {question_uniq_id}")
    # Record
    record_db = crud_record.get(db=db, uniq_id=question_meta_db.record_uniq_id)
    if not record_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Record not found: {question_meta_db.record_uniq_id} for question {question_uniq_id}")
    # Commentar
    commentar_db = crud_commentar.get(db=db, uniq_id=question_meta_db.commentar_uniq_id)
    if not commentar_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Record not found: {question_meta_db.commentar_uniq_id} for question {question_uniq_id}")
    
    return s_question.QuestionCombineGet(
        commentar=commentar_db,
        question=question_meta_db,
        read_text=read_text_db,
        record=record_db
    )


@router.post("/combine", response_model=s_question.QuestionCombineGet)
def create_question_combine(
    *,
    db: Session = Depends(deps.get_db),
    owner_uniq_id: UUID = Form(...),
    topic_uniq_id: UUID = Form(...),
    file: UploadFile = File(...), file_extension: str = Form(...),
    read_text: str = Form(...),
    commentar: str = Form(...),
) -> Any:
    # Check existing question for topic
    question_meta_db = crud_question.get_meta_by_topic_uniq_id(
        db=db, topic_uniq_id=topic_uniq_id
    )
    if question_meta_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Question existed for topic uniq id: {topic_uniq_id}"
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
    # Read text
    read_text_db = crud_small.crud_read_text.create(
        db=db, obj_in=s_small.ReadTextCreate(owner_uniq_id=owner_uniq_id, read_text=read_text)
    )
    # Question meta
    question_meta_db = crud_question.create(
        db=db, obj_in=s_question.QuestionMetaCreate(
            topic_uniq_id=topic_uniq_id, owner_uniq_id=owner_uniq_id,
            commentar_uniq_id=commentar_db.uniq_id,
            read_text_uniq_id=read_text_db.uniq_id,
            record_uniq_id=record_db.uniq_id,
        )
    )
    return s_question.QuestionCombineGet(
        question=question_meta_db, commentar=commentar_db,
        read_text=read_text_db, record=record_db,
    )


# @router.delete("/{question_uniq_id}", response_model=s_question.QuestionGet)
# def delete_question_by_uniq_id(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_uniq_id: UUID,
#     # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
# ) -> Any:
#     # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     question_db = crud_question.get(db=db, uniq_id=question_uniq_id)
#     if not question_db:
#         raise HTTPException(status_code=404, detail="Question not found")
#     question_db = crud_question.remove(db=db, uniq_id=question_uniq_id)
#     return question_db


# @router.put("/{question_uniq_id}", response_model=s_question.QuestionGet)
# def update_question_by_uniq_id(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_uniq_id: UUID,
#     question_in: s_question.QuestionUpdate,
#     # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
# ) -> Any:
#     # Check permission
#     # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     question_db = crud_question.crud_question.get(db=db, uniq_id=question_uniq_id)
#     if not question_db:
#         raise HTTPException(status_code=404, detail="Question not found")
#     # Check if there existed a question with same name
#     question_db_with_same_new_name = crud_question.crud_question.get_question_by_question_name(db=db, question_name=question_in.question_name)
#     if question_db_with_same_new_name:
#         if question_db_with_same_new_name.question_name != question_in.question_name:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=f"Couldn't change question name: Question name existed: {question_in.question_name}"
#             )
#     question_db = crud_question.crud_question.update(db=db, db_obj=question_db, obj_in=question_in)
#     return question_db


# @router.delete("/{question_uniq_id}", response_model=s_question.QuestionGet)
# def delete_question_by_uniq_id(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_uniq_id: UUID,
#     # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
# ) -> Any:
#     # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     question_db = crud_question.crud_question.get(db=db, uniq_id=question_uniq_id)
#     if not question_db:
#         raise HTTPException(status_code=404, detail="Question not found")
#     question_db = crud_question.crud_question.remove(db=db, uniq_id=question_uniq_id)
#     return question_db


# @router.get("/for-user/{user_uniq_id}", response_model=List[s_question.QuestionGet])
# def get_all_questions_for_user_uniq_id(
#     *, db: Session = Depends(deps.get_db), user_uniq_id: UUID
# ) -> Any:
#     user_questions = crud_question.crud_user_question.get_questions_of_user(
#         db=db, user_uniq_id=user_uniq_id)
#     return user_questions