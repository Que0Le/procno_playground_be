import os
import string
import random
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile, Cookie
from sqlalchemy.orm import Session

from app.crud import crud_answer, crud_question, crud_small, crud_topic
from app.models import m_user
from app.schemas import s_topic
from app.crud import *
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/own-topics/", status_code=status.HTTP_201_CREATED)
async def create_new_topic(
        *,
        db: Session = Depends(deps.get_db),
        current_user: m_user.UserDB = Depends(deps.get_current_user),
        file: UploadFile = File(...), topic_title: str = Form(...),
        source_language: str = Form(...), source_level: str = Form(...),
        wish_correct_languages: str = Form(...), tags: str = Form(...),
        readtext: str = Form(...), commentar: str = Form(...),
):

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

    topic_create = s_topic.TopicCreate(
        topic_title=topic_title,
        source_language=source_language,
        source_level=source_level,
        wish_correct_languages=[x.strip() for x in wish_correct_languages.split(',')],
        #
        owner_uniq_id=str(current_user.uniq_id),
        owner_username=str(current_user.username),
        #
        tags=[x.strip() for x in tags.split(',')],
        #
        readtext=readtext,
        #
        record_filename=filename,
        #
        commentar=commentar,
    )

    """ Write new topic to DB """
    # Add to topic table
    topic_db = crud_topic.crud_topic.create_topic(db=db, topic_create=topic_create)

    # Add tags and relation with topic
    tag_db_s = []
    tag_topic_db_s = []
    for tag_name in topic_create.tags:
        tag_db = crud_small.crud_tag.create_tag(db=db, tag_name=tag_name, description="")
        tag_db_s.append(tag_db)
        #
        tag_topic_db = crud_small.crud_tag_topic.create_tag_topic_relation(
            db=db,
            topic_uniq_id=topic_db.uniq_id, tag_uniq_id=tag_db.uniq_id
        )
        tag_topic_db_s.append(tag_topic_db)

    # Add record
    record_db = crud_small.crud_record.create_record(
        db=db,
        filename=topic_create.record_filename,
        owner_uniq_id=topic_create.owner_uniq_id
    )
    # Add read text
    readtext_db = crud_small.crud_read_text.create_read_text(
        db=db,
        read_text_from_user=topic_create.readtext,
        owner_uniq_id=topic_create.owner_uniq_id
    )
    # Add commentar
    commentar_db = crud_small.crud_commentar.create_commentar(
        db=db,
        commentar_from_user=topic_create.commentar,
        owner_uniq_id=topic_create.owner_uniq_id
    )

    # Add question and relation with topic
    question_db = crud_question.crud_question.create_question(
        db=db,
        owner_uniq_id=topic_create.owner_uniq_id,
        commentar_uniq_id=commentar_db.uniq_id,
        record_uniq_id=record_db.uniq_id,
        text_uniq_id=readtext_db.uniq_id
    )
    topic_question_db = crud_topic.crud_topic_question.create_topic_question_relation(
        db=db,
        topic_uniq_id=topic_db.uniq_id, question_uniq_id=question_db.uniq_id
    )

    """ Write file """
    with open(f"./data/records/{filename}", "wb+") as f:
        f.write(file.file.read())

    """ Now try retrieve the recently added topic """
    topic_db = crud_topic.crud_topic.get_combi_by_topic_uniq_id(
        db=db, topic_uniq_id=topic_db.uniq_id
    )
    topic_get = s_topic.create_topic_combi_from_db_model(topic_db)

    return {
        "status": "success",
        "topic": topic_get
    }


@router.get(
    "/own-topics/",
    response_model=List[s_topic.TopicOverviewGet],
    status_code=status.HTTP_200_OK
)
def get_own_topic_overviews(
        db: Session = Depends(deps.get_db),
        current_user: m_user.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Get topic overviews created by current user
    """
    topics_db = crud_topic.crud_topic.get_combi_by_user_id(
        db=db, owner_uniq_id=current_user.uniq_id
    )
    r = []
    for topic_db in topics_db:
        temp = s_topic.create_topic_combi_from_db_model(topic_db)
        if temp:
            r.append(temp)
    return r


@router.delete("/uniq_id/{uniq_id}", status_code=status.HTTP_200_OK)
def delete_topic_and_related_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    # current_user: models.UserDB = Depends(deps.get_current_user),
    uniq_id: str
) -> Any:
    """
    Delete topic, including question, answers and related
    """
    topic_db = crud_topic.crud_topic.get_combi_by_topic_uniq_id(
        db=db, topic_uniq_id=uniq_id
    )
    if not topic_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found!"
        )

    # Stupid db cursor: answer_combi_db will be invalid when
    # next expression that requires cursor gets executed.
    # Solution: create copies of data.
    topic_get = s_topic.create_topic_combi_from_db_model(topic_db)

    # if str(topic_db.u_uniq_id) != str(current_user.uniq_id):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not owner or admin"
    #     )

    # Delete answers related rows:
    answer_combi_s = crud_answer.crud_answer.get_combi_by_topic_uniq_id(
        db=db, topic_uniq_id=str(topic_db.t_uniq_id)
    )
    ans_uniq_id_s = []
    rc_uniq_id_s = []
    c_uniq_id_s = []
    for answer_combi in answer_combi_s:
        ans_uniq_id_s.append(str(answer_combi.ans_uniq_id))
        rc_uniq_id_s.append(str(answer_combi.rc_uniq_id))
        c_uniq_id_s.append(str(answer_combi.c_uniq_id))
    # Delete in topic_answer
    nbr_topics_answer_deleted = crud_topic.crud_topic_answer.remove_by_topic_uniq_id(
        db=db, topic_uniq_id=str(topic_db.t_uniq_id)
    )
    # Delete in answers
    nbr_answers_deleted = crud_answer.crud_answer.remove_by_uniq_id_s(
        db=db, uniq_id_s=ans_uniq_id_s
    )
    if nbr_answers_deleted != nbr_topics_answer_deleted:
        print("nbr_answers_deleted != nbr_topics_answer_deleted")
        # TODO: more serious error handling and logging
    for rc_uniq_id in rc_uniq_id_s:
        # Delete record
        record = crud_small.crud_record.remove(db=db, uniq_id=rc_uniq_id)
        if os.path.isfile("./data/records/" + record.filename):
            os.remove("./data/records/" + record.filename)
    for c_uniq_id in c_uniq_id_s:
        # Delete commentar
        commentar = crud_small.crud_commentar.remove(db=db, uniq_id=c_uniq_id)

    # Delete question:
    # Delete topic_question
    topic_question = crud_topic.crud_topic_question.remove_by_topic_uniq_id(
        db=db, topic_uniq_id=str(topic_db.t_uniq_id)
    )
    # Delete question
    question = crud_question.crud_question.remove(
        db=db, uniq_id=str(topic_db.q_uniq_id)
    )
    # Delete record
    record = crud_small.crud_record.remove(db=db, uniq_id=str(topic_db.rc_uniq_id))
    if os.path.isfile("./data/records/" + record.filename):
        os.remove("./data/records/" + record.filename)
    # Delete readtext
    read_text = crud_small.crud_read_text.remove(db=db, uniq_id=str(topic_db.rt_uniq_id))
    # Delete commentar
    commentar = crud_small.crud_commentar.remove(db=db, uniq_id=str(topic_db.c_uniq_id))

    # Delete tag topic
    tag_topic_s = crud_small.crud_tag_topic.remove_by_topic_uniq_id(
        db=db, topic_uniq_id=str(topic_db.t_uniq_id)
    )
    print(tag_topic_s)
    # Delete topic
    topic = crud_topic.crud_topic.remove(db=db, uniq_id=str(topic_db.t_uniq_id))

    return {"status": "success", "topic": topic_get}


@router.get("/uniq_id/{uniq_id}", response_model=s_topic.TopicOverviewGet, status_code=200)
def get_topic_overview_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    uniq_id: str,
    cookie_name: Optional[str] = Cookie(None)
) -> Any:
    """
    Get a topic by its uniq_id
    """
    topic_db = crud_topic.crud_topic.get_combi_by_topic_uniq_id(db=db, topic_uniq_id=uniq_id)
    topic_get = s_topic.create_topic_combi_from_db_model(topic_db)
    return topic_get
