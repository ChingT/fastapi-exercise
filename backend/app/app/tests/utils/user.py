from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.token_utils import TokenType, create_token
from app.crud.user import crud_user
from app.models.user import User, UserCreate


async def create_test_user(session: AsyncSession, is_superuser: bool = False) -> User:
    email = settings.TEST_USER_EMAIL
    user = await crud_user.get_by_email(session, email)
    if user is None:
        user_in = UserCreate(email=email, password=settings.TEST_USER_PASSWORD)
        user = await crud_user.create(session, user_in, is_superuser=is_superuser)
    await crud_user.activate(session, user)
    return user


async def get_user_authentication_headers(user: User) -> dict[str, str]:
    access_token = create_token(
        user.id, settings.ACCESS_TOKEN_EXPIRE_HOURS, TokenType.ACCESS
    )
    return {"Authorization": f"Bearer {access_token}"}
