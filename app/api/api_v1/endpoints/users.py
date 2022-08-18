from typing import Any, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Cookie
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from fastapi.responses import JSONResponse
from app.crud import crud_user

# from app import crud, models, schemas
from app.models import *
from app.models import m_user
from app.schemas import *
from app.crud import *
from app.api import deps
from app.core.config import settings
from app.schemas import s_user


router = APIRouter()


@router.get("/", response_model=List[s_user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud_user.crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=s_user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: s_user.UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud_user.crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.crud_user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=s_user.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    username: str = Body(None),
    email: EmailStr = Body(None),
    current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = s_user.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if username is not None:
        user_in.username = username
    if email is not None:
        user_in.email = email
    user = crud_user.crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=s_user.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: m_user.UserDB = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=s_user.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    username: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud_user.crud_user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = s_user.UserCreate(password=password, email=email, username=username)
    user = crud_user.crud_user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=s_user.User)
def read_user_by_id(
    user_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud_user.crud_user.get(db, id=user_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return user


@router.put("/{user_id}", response_model=s_user.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: s_user.UserUpdate,
    current_user: m_user.UserDB = Depends(deps.get_current_user),
) -> Any:
    """
    Update a user.
    """
    user = crud_user.crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    elif user.email!=current_user.email:
        raise HTTPException(
            status_code=401,
            detail="Not authorized",
        )
    user = crud_user.crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
