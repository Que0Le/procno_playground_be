from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token/", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(
        user.uniq_id, expires_delta=access_token_expires
    )
    response = JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "uniq_id": str(user.uniq_id),
    })

    """
    Secure - cookie must be transmitted over HTTPS
    HTTP Only - cookies are only accessible from a server
    Same Site - prevents the cookie from being sent in cross-site requests
    """
    # print(str(settings.COOKIES_SECURE) + str(settings.COOKIES_HTTP_ONLY) + str(settings.COOKIES_SAME_SITE))
    response.set_cookie(
        key="procno_cookie_token",
        value=token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        path=settings.COOKIES_PATH,
        domain=settings.COOKIES_DOMAIN,
        secure=settings.COOKIES_SECURE,
        httponly=settings.COOKIES_HTTP_ONLY,
        samesite=settings.COOKIES_SAME_SITE,
    )
    response.set_cookie(
        key="procno_token_expiration",
        value=str(
            datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ).split(".")[0].replace("-", "_").replace(":", "_").replace(" ", "___"),
        max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        path=settings.COOKIES_PATH,
        domain=settings.COOKIES_DOMAIN,
        secure=settings.COOKIES_SECURE,
        httponly=False,
        samesite=settings.COOKIES_SAME_SITE,
    )
    return response


@router.delete("/login/access-token/")
def remove_token(
        current_user: models.UserDB = Depends(deps.get_current_user)
) -> Any:
    """
    Delete token-cookie (cookie-based transport),
    and/or remove token from server's book (header based)
    """
    # TODO: remove token from storage

    content = {"status": "success"}
    if current_user:
        content["current_user"] = jsonable_encoder(
            schemas.User(
                id=current_user.id,
                email=EmailStr(current_user.email),
                username=current_user.username,
                is_active=current_user.is_active,
            )
        )
    response = JSONResponse(content=content)
    """
    Same Site - prevents the cookie from being sent in cross-site requests
    HTTP Only - cookies are only accessible from a server
    Secure - cookie must be transmitted over HTTPS
    """
    response.delete_cookie(key="procno_cookie_token")
    response.delete_cookie(key="procno_token_expiration")
    response.status_code = status.HTTP_200_OK
    return response


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.UserDB = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
