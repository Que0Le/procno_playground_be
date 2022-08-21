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
from app.crud.crud_question import crud_question
from app.crud.crud_topic import crud_topic
from app.crud.crud_small import crud_commentar, crud_record, crud_read_text
from app.models import *
from app.models import m_user
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_question
from app.utilities import utils, strings, files_and_dir


router = APIRouter()


# @router.get("/test", response_model=s_question.ArticleResponse)
# def test(
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     u = s_question.User()
#     a = s_question.Article()
#     ar = s_question.ArticleResponse(article=a, author=u)
#     return s_question.ArticleResponse(article=a, author=u)

""" QUESTIONS """


@router.get("/", response_model=List[s_question.QuestionGet])
def get_all_questions(
    db: Session = Depends(deps.get_db),
) -> Any:
    questions_db = crud_question.get_multi(db=db)
    return questions_db


# @router.post("/", response_model=s_question.QuestionGet)
# def create_question(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_in: s_question.QuestionCreate,
#     # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
# ) -> Any:
#     question_db = crud_question.get_question_by_topic_uniq_id(
#         db=db, topic_uniq_id=question_in.topic_uniq_id
#     )
#     if question_db:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail=f"Question existed for topic uniq id: {question_in.topic_uniq_id}"
#         )
#     question_db = crud_question.create(db=db, obj_in=question_in)
#     return question_db


# @router.get("/{question_uniq_id}", response_model=s_question.QuestionGet)
# def get_question_by_uniq_id(
#     *,
#     db: Session = Depends(deps.get_db),
#     question_uniq_id: UUID,
# ) -> Any:
#     question_db = crud_question.get(db=db, uniq_id=question_uniq_id)
#     if not question_db:
#         raise HTTPException(status_code=404, detail=f"Question not found: {question_uniq_id}")
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