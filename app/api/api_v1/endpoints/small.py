import os
from typing import Any, List
from datetime import datetime
import random
import string

from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_small

from app.models import *
from app.models import m_user
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_small
from app.utilities import utils

router_roles = APIRouter()
router_tags = APIRouter()


@router_roles.get("/", response_model=List[s_small.RoleGet])
def get_all_roles(
    db: Session = Depends(deps.get_db),
) -> Any:
    roles = crud_small.crud_role.get_multi(db=db)
    return roles


@router_roles.post("/", response_model=s_small.RoleGet)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: s_small.RoleCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    role_db = crud_small.crud_role.create(db=db, obj_in=role_in)
    return role_db


@router_roles.put("/{role_uniq_id}", response_model=s_small.RoleGet)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    role_uniq_id: str,
    role_in: s_small.RoleUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    role_db = crud_small.crud_role.get(db=db, uniq_id=role_uniq_id)
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    role_db = crud_small.crud_role.update(db=db, db_obj=role_db, obj_in=role_in)
    return role_db


@router_roles.delete("/{role_uniq_id}", response_model=s_small.RoleGet)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    role_uniq_id: str,
    role_in: s_small.RoleUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    role_db = crud_small.crud_role.get(db=db, uniq_id=role_uniq_id)
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    role_db = crud_small.crud_role.remove(db=db, uniq_id=role_uniq_id)
    return role_db


@router_roles.get("/for-user/{user_uniq_id}")
def get_all_roles_for_user(
    *, db: Session = Depends(deps.get_db), user_uniq_id: str
) -> List[s_small.UserRoleGet]:
    if not utils.is_valid_uuid(user_uniq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Couldn't process UUID : {user_uniq_id}",
        )
    user_roles = crud_small.crud_user_role.get_roles_of_user(
        db=db, user_uniq_id=user_uniq_id)
    return user_roles


""" TAG """


@router_tags.get("/", response_model=List[s_small.TagGet])
def get_all_tags(
    db: Session = Depends(deps.get_db),
) -> Any:
    tags = crud_small.crud_tag.get_multi(db=db)
    return tags


@router_tags.get("/for-topic/{topic_uniq_id}")
def get_all_tags_for_topic(
    *, db: Session = Depends(deps.get_db), topic_uniq_id: str
) -> List[s_small.TagTopicGet]:
    if not utils.is_valid_uuid(topic_uniq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Couldn't process UUID : {topic_uniq_id}",
        )
    tags_topic = crud_small.crud_tag_topic.get_tags_of_topic(
        db=db, topic_uniq_id=topic_uniq_id)
    return tags_topic
