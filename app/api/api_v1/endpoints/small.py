import os
from typing import Any, List
from datetime import datetime
import random
import string

from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud_small

from app.models import *
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_small
from app.utilities import utils

router_roles = APIRouter()


@router_roles.get("/")
def get_all_roles(
    db: Session = Depends(deps.get_db),
) -> List[s_small.RoleGet]:
    roles = crud_small.crud_role.get_multi(db=db)
    return roles


@router_roles.get("/for-user/{user_uniq_id}")
def get_all_roles(
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
