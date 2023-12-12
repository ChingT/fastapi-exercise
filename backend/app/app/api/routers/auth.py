import time
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.security import (
    JWT_ALGORITHM,
    JWTTokenPayload,
    generate_access_token_response,
    verify_password,
)
from app.models import User
from app.schemas.auth import AccessTokenResponse, RefreshTokenRequest

router = APIRouter()

FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/access-token", status_code=status.HTTP_201_CREATED)
def login_access_token(db: SessionDep, form_data: FormDataDep) -> AccessTokenResponse:
    """Get an access token for future requests using username and password."""
    result = db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    return generate_access_token_response(user.id)


@router.post("/refresh-token", status_code=status.HTTP_201_CREATED)
def refresh_token(db: SessionDep, token: RefreshTokenRequest) -> AccessTokenResponse:
    """Get an access token for future requests using refresh token."""
    try:
        payload = jwt.decode(
            token.refresh_token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
    except jwt.DecodeError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials. Decode error.",
        ) from err

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = JWTTokenPayload(**payload)
    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials. Cannot use access token.",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    user = db.get(User, token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return generate_access_token_response(user.id)
