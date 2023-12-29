from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud.user import crud_user
from app.models.user import User, UserCreate, UserUpdatePassword

from .utils import random_email, random_lower_string


async def get_user_authentication_headers(
    client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}
    r = await client.post("/auth/access-token", data=data)
    response = r.json()
    return {"Authorization": f"Bearer {response['access_token']}"}


async def get_superuser_authentication_headers(client: AsyncClient) -> dict[str, str]:
    data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post("/auth/access-token", data=data)
    response = r.json()
    return {"Authorization": f"Bearer {response['access_token']}"}


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    return await crud_user.create(db, user_in)


async def get_authentication_token_from_email(
    db: AsyncSession, client: AsyncClient, email: str
) -> dict[str, str]:
    """Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await crud_user.get_by_email(db, email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = await crud_user.create(db, user_in_create)
    else:
        user_in_update = UserUpdatePassword(password=password)
        user = await crud_user.update(db, user, user_in_update)

    await crud_user.activate(db, user)
    return await get_user_authentication_headers(client, email, password)
