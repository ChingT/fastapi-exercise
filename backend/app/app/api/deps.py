from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.utils import (
    credentials_exception,
    inactive_user_exception,
    no_permissions_exception,
    user_not_found_exception,
)
from app.core.token_utils import TokenType, decode_token
from app.db.session import SessionLocal
from app.models.user import User


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    if user_id := decode_token(token, TokenType.ACCESS):
        if user := await session.get(User, user_id):
            return user
        raise user_not_found_exception
    raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise inactive_user_exception
    return current_user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


async def get_current_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise no_permissions_exception
    return current_user
