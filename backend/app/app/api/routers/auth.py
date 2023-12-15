from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, SessionDep
from app.core.token_utils import (
    credentials_exception,
    decode_token,
    generate_tokens_response,
)
from app.crud.user import crud_user
from app.models.user import UserOut, UserUpdatePassword
from app.schemas.auth import RefreshTokenRequest, TokensResponse

router = APIRouter()

FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/access-token", status_code=status.HTTP_201_CREATED)
def login_access_token(db: SessionDep, form_data: FormDataDep) -> TokensResponse:
    """Get an access token for future requests using username and password."""
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return generate_tokens_response(user.id)


@router.post("/refresh-token", status_code=status.HTTP_201_CREATED)
def refresh_token(db: SessionDep, token: RefreshTokenRequest) -> TokensResponse:
    """Get an access token using a refresh token."""
    if user := decode_token(db, token.refresh_token, is_refresh=True):
        return generate_tokens_response(user.id)
    raise credentials_exception


@router.post("/reset-password", status_code=status.HTTP_201_CREATED)
def reset_password(
    db: SessionDep,
    current_user: CurrentUser,
    updated_password: UserUpdatePassword,
) -> UserOut:
    """Update current user password."""
    return crud_user.update(db, db_obj=current_user, obj_in=updated_password)
