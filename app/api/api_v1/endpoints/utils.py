from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas, crud
from app.api import deps
from app.core.celery_app import celery_app
from app.utils import send_test_email
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    # current_user: models.UserDB = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    # current_user: models.UserDB = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}

@router.post("/test-any/", response_model=schemas.Msg, status_code=201)
def test_any(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Test anything.
    """
    print(crud.tag_topic.get_topic_ids_by_tag_id(db=db, tag_id=10))

    return {"msg": "Test request sent"}
