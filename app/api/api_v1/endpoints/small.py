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

from app.models import *
from app.models import m_user
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_small
from app.utilities import utils, strings, files_and_dir

router_roles = APIRouter()
router_tags = APIRouter()
router_records = APIRouter()
router_commentars = APIRouter()

# TODO: clean input


""" ROLES """


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
    role_uniq_id: UUID,
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
    role_uniq_id: UUID,
    role_in: s_small.RoleUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # Check permission
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    role_db = crud_small.crud_role.get(db=db, uniq_id=role_uniq_id)
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")
    # Check if there existed a role with same name
    role_db_with_same_new_name = crud_small.crud_role.get_role_by_role_name(db=db, role_name=role_in.role_name)
    if role_db_with_same_new_name:
        if role_db_with_same_new_name.role_name != role_in.role_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Couldn't change role name: Role name existed: {role_in.role_name}"
            )
    role_db = crud_small.crud_role.update(db=db, db_obj=role_db, obj_in=role_in)
    return role_db


@router_roles.delete("/{role_uniq_id}", response_model=s_small.RoleGet)
def delete_role_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    role_uniq_id: UUID,
    role_in: s_small.RoleUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    role_db = crud_small.crud_role.get(db=db, uniq_id=role_uniq_id)
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")
    role_db = crud_small.crud_role.remove(db=db, uniq_id=role_uniq_id)
    return role_db


@router_roles.get("/for-user/{user_uniq_id}", response_model=List[s_small.RoleGet])
def get_all_roles_for_user_uniq_id(
    *, db: Session = Depends(deps.get_db), user_uniq_id: UUID
) -> Any:
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
    tag_uniq_id: UUID,
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
    tag_uniq_id: UUID,
    tag_in: s_small.TagUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    tag_db = crud_small.crud_tag.get(db=db, uniq_id=tag_uniq_id)
    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_db_with_same_new_name = crud_small.crud_tag.get_tag_by_tag_name(db=db, tag_name=tag_in.tag_name)
    if tag_db_with_same_new_name:
        if tag_db_with_same_new_name.tag_name != tag_in.tag_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Couldn't change tag name: Tag existed: {tag_in.tag_name}"
            )
    tag_db = crud_small.crud_tag.update(db=db, db_obj=tag_db, obj_in=tag_in)
    return tag_db


@router_tags.delete("/{tag_uniq_id}", response_model=s_small.TagGet)
def delete_tag_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    tag_uniq_id: UUID,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    tag_db = crud_small.crud_tag.get(db=db, uniq_id=tag_uniq_id)
    if not tag_db:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_db = crud_small.crud_tag.remove(db=db, uniq_id=tag_uniq_id)
    return tag_db


@router_tags.get("/for-topic/{topic_uniq_id}", response_model=List[s_small.TagGet])
def get_all_tags_for_topic_uniq_id(
    *, db: Session = Depends(deps.get_db), topic_uniq_id: UUID
) -> Any:
    if not utils.is_valid_uuid(topic_uniq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Couldn't process UUID : {topic_uniq_id}",
        )
    tags_db = crud_small.crud_tag_topic.get_tags_of_topic(
        db=db, topic_uniq_id=topic_uniq_id)
    return tags_db


""" RECORDS """

@router_records.get("/", response_model=List[s_small.RecordGet])
def get_all_records(
    db: Session = Depends(deps.get_db),
) -> Any:
    records_db = crud_small.crud_record.get_multi(db=db)
    return records_db


@router_records.get("/{record_uniq_id}", response_model=s_small.RecordGet)
def get_record_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    record_uniq_id: UUID,
) -> Any:
    """
    Same as return record meta, cause we can not send both text and file byte.
    Client request file separately later.
    """
    record_db = crud_small.crud_record.get(db=db, uniq_id=record_uniq_id)
    if not record_db:
        raise HTTPException(status_code=404, detail=f"Record not found in db: {record_uniq_id}")
    return record_db


@router_records.post("/", response_model=s_small.RecordGet)
def create_record(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...), 
    file_extension: str = Form(...), owner_uniq_id: Optional[UUID] = Form(...),
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    """ Create meta data and write to file. Filename holds extension in this request! """
    # TODO: Check write and uniq_id assigning privillege.
    tries = 10
    filename = ""
    while tries > 0:
        filename = strings.random_alphanumeric(length=32)
        if not os.path.isfile(f"{settings.DATA_PATH}/records/" + filename):
            record_db = crud_small.crud_record.get_record_by_filename(db=db, filename=filename)
            if not record_db:
                break
        tries = tries - 1
        if tries == 0:
            print("Failed create filename")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Fail create filename"
            )
    # TODO: check filename extension
    filename = filename + "." + file_extension
    # Write to data folder
    with open(f"{settings.DATA_PATH}/records/{filename}", "wb+") as f:
        f.write(file.file.read())
    # Wite to db
    record_in = s_small.RecordCreate(filename=filename, owner_uniq_id=owner_uniq_id)
    record_db = crud_small.crud_record.create(db=db, obj_in=record_in)
    return record_db


@router_records.delete("/{record_uniq_id}", response_model=s_small.RecordGet)
def delete_record_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    record_uniq_id: UUID,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # TODO: check permission
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    record_db = crud_small.crud_record.get(db=db, uniq_id=record_uniq_id)
    if not record_db:
        raise HTTPException(status_code=404, detail="Record not found in database")

    record_db = crud_small.crud_record.remove(db=db, uniq_id=record_uniq_id)
    try:
        os.remove(f"{settings.DATA_PATH}/records/{record_db.filename}")
    except FileNotFoundError as not_found:
        print(not_found.filename)

    return record_db


@router_records.post("/meta-record", response_model=s_small.RecordGet)
def create_meta_record(
    *,
    db: Session = Depends(deps.get_db),
    record_in: s_small.RecordCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    """ Only create meta data in DB. Filename holds extension in this request! """
    # TODO: Check write and uniq_id assigning privillege.
    tries = 10
    filename = ""
    while tries > 0:
        filename = strings.random_alphanumeric(length=32)
        if not os.path.isfile(f"{settings.DATA_PATH}/records/" + filename):
            record_db = crud_small.crud_record.get_record_by_filename(db=db, filename=filename)
            if not record_db:
                break
        tries = tries - 1
        if tries == 0:
            print("Failed create filename")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Fail create filename"
            )
    record_in.filename = filename + "." + record_in.filename
    record_db = crud_small.crud_record.create(db=db, obj_in=record_in)
    return record_db


@router_records.get("/meta-record/{record_uniq_id}", response_model=s_small.RecordGet)
def get_meta_record_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    record_uniq_id: UUID,
) -> Any:
    record_db = crud_small.crud_record.get(db=db, uniq_id=record_uniq_id)
    if not record_db:
        raise HTTPException(status_code=404, detail=f"Record not found in db: {record_uniq_id}")
    return record_db


# @router_records.put("/{record_uniq_id}", response_model=s_small.RecordGet)
# def update_record_by_uniq_id(
#     *,
#     db: Session = Depends(deps.get_db),
#     record_uniq_id: str,
#     record_in: s_small.RecordUpdate,
#     # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
# ) -> Any:
#     # Check permission
#     # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
#     #     raise HTTPException(status_code=400, detail="Not enough permissions")
#     record_db = crud_small.crud_record.get(db=db, uniq_id=record_uniq_id)
#     if not record_db:
#         raise HTTPException(status_code=404, detail="Record not found")
#     # Check if there existed a record with same name
#     record_db_with_same_new_name = crud_small.crud_record.get_record_by_record_name(db=db, record_name=record_in.record_name)
#     if record_db_with_same_new_name:
#         if record_db_with_same_new_name.record_name != record_in.record_name:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=f"Couldn't change record name: Record name existed: {record_in.record_name}"
#             )
#     record_db = crud_small.crud_record.update(db=db, db_obj=record_db, obj_in=record_in)
#     return record_db


@router_records.get("/meta-records-for-user/{user_uniq_id}", response_model=List[s_small.RecordGet])
def get_all_meta_records_for_user_uniq_id(
    *, db: Session = Depends(deps.get_db), user_uniq_id: UUID
) -> Any:
    user_records_db = crud_small.crud_record.get_records_of_user_by_uniq_id(
        db=db, user_uniq_id=user_uniq_id
    )
    return user_records_db


""" COMMENTARS """

@router_commentars.get("/", response_model=List[s_small.CommentarGet])
def get_all_commentars(
    db: Session = Depends(deps.get_db),
) -> Any:
    commentars_db = crud_small.crud_commentar.get_multi(db=db)
    return commentars_db


@router_commentars.get("/{commentar_uniq_id}", response_model=s_small.CommentarGet)
def get_all_commentars(
    *,
    db: Session = Depends(deps.get_db),
    commentar_uniq_id: UUID,
) -> Any:
    commentar_db = crud_small.crud_commentar.get(db=db, uniq_id=commentar_uniq_id)
    if not commentar_db:
        raise HTTPException(status_code=404, detail=f"Commentar not found: {commentar_uniq_id}")
    return commentar_db


@router_commentars.post("/", response_model=s_small.CommentarGet)
def create_commentar(
    *,
    db: Session = Depends(deps.get_db),
    commentar_in: s_small.CommentarCreate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    commentar_db = crud_small.crud_commentar.create(db=db, obj_in=commentar_in)
    return commentar_db


@router_commentars.put("/{commentar_uniq_id}", response_model=s_small.CommentarGet)
def update_commentar_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    commentar_uniq_id: UUID,
    commentar_in: s_small.CommentarUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # Check permission
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    commentar_db = crud_small.crud_commentar.get(db=db, uniq_id=commentar_uniq_id)
    if not commentar_db:
        raise HTTPException(status_code=404, detail="Commentar not found")
    commentar_db = crud_small.crud_commentar.update(db=db, db_obj=commentar_db, obj_in=commentar_in)
    return commentar_db


@router_commentars.delete("/{commentar_uniq_id}", response_model=s_small.CommentarGet)
def delete_commentar_by_uniq_id(
    *,
    db: Session = Depends(deps.get_db),
    commentar_uniq_id: UUID,
    commentar_in: s_small.CommentarUpdate,
    # current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    commentar_db = crud_small.crud_commentar.get(db=db, uniq_id=commentar_uniq_id)
    if not commentar_db:
        raise HTTPException(status_code=404, detail="Commentar not found")
    commentar_db = crud_small.crud_commentar.remove(db=db, uniq_id=commentar_uniq_id)
    return commentar_db


@router_commentars.get("/for-user/{user_uniq_id}")
def get_all_commentars_for_user_uniq_id(
    *, db: Session = Depends(deps.get_db), user_uniq_id: UUID
) -> List[s_small.CommentarGet]:
    if not utils.is_valid_uuid(user_uniq_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Couldn't process UUID : {user_uniq_id}",
        )
    user_commentars = crud_small.crud_commentar.get_commentars_of_user_by_uniq_id(
        db=db, user_uniq_id=user_uniq_id)
    return user_commentars

