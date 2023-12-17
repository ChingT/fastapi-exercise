from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.utils import (
    credentials_exception,
    inactive_user_exception,
    no_permissions_exception,
    user_not_found_exception,
)
from app.core.token_utils import decode_token
from app.db.database import SessionLocal
from app.models.auth import TokenType
from app.models.user import User


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_db)]
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def get_current_user(db: SessionDep, token: TokenDep) -> User:
    if user_id := decode_token(token, TokenType.ACCESS):
        if user := db.get(User, user_id):
            return user
        raise user_not_found_exception
    raise credentials_exception


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise inactive_user_exception
    return current_user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


def get_current_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise no_permissions_exception
    return current_user
