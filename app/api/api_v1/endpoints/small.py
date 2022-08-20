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
    roles_db = crud_small.crud_role.get_multi(db=db)
    return roles_db


@router_roles.get("/{role_uniq_id}", response_model=s_small.RoleGet)
def get_all_roles(
    *,
    db: Session = Depends(deps.get_db),
    role_uniq_id: str,
) -> Any:
    role_db = crud_small.crud_role.get(db=db, uniq_id=role_uniq_id)
    if not role_db:
        raise HTTPException(status_code=404, detail=f"Role not found: {role_uniq_id}")
    return role_db


@router_roles.post("/", response_model=s_small.RoleGet)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: s_small.RoleCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    role_db = crud_small.crud_role.get_role_by_role_name(db=db, role_name=role_in.role_name)
    if role_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Role existed: {role_in.role_name}"
        )
    role_db = crud_small.crud_role.create(db=db, obj_in=role_in)
    return role_db


@router_roles.put("/{role_uniq_id}", response_model=s_small.RoleGet)
def update_role_by_uniq_id(
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
def delete_role_by_uniq_id(
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
def get_all_roles_for_user_uniq_id(
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
    tags_db = crud_small.crud_tag.get_multi(db=db)
    return tags_db


@router_tags.get("/{tag_uniq_id}", response_model=s_small.TagGet)
def get_all_tags(
    *,
    db: Session = Depends(deps.get_db),
    tag_uniq_id: str,
) -> Any:
    tag_db = crud_small.crud_tag.get(db=db, uniq_id=tag_uniq_id)
    if not tag_db:
        raise HTTPException(status_code=404, detail=f"Tag not found: {tag_uniq_id}")
    return tag_db


@router_tags.post("/", response_model=s_small.TagGet)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: s_small.TagCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    tag_db = crud_small.crud_tag.get_tag_by_tag_name(db=db, tag_name=tag_in.tag_name)
    if tag_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Tag existed: {tag_in.tag_name}"
        )
    tag_db = crud_small.crud_tag.create(db=db, obj_in=tag_in)
    return tag_db


@router_tags.put("/{tag_uniq_id}", response_model=s_small.TagGet)
def update_tag_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    tag_uniq_id: str,
    tag_in: s_small.TagUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    tag_db = crud_small.crud_tag.get(db=db, uniq_id=tag_uniq_id)
    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    tag_db = crud_small.crud_tag.update(db=db, db_obj=tag_db, obj_in=tag_in)
    return tag_db


@router_tags.delete("/{tag_uniq_id}", response_model=s_small.TagGet)
def delete_tag_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    tag_uniq_id: str,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    tag_db = crud_small.crud_tag.get(db=db, uniq_id=tag_uniq_id)
    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    tag_db = crud_small.crud_tag.remove(db=db, uniq_id=tag_uniq_id)
    return tag_db


@router_tags.get("/for-topic/{topic_uniq_id}")
def get_all_tags_for_topic_uniq_id(
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