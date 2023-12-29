import pytest
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import verify_password
from app.crud.user import crud_user
from app.models.user import UserCreate, UserUpdatePassword
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.anyio()
async def test_create_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


@pytest.mark.anyio()
async def test_authenticate_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    authenticated_user = await crud_user.authenticate(db, email, password)
    assert authenticated_user
    assert user.email == authenticated_user.email


@pytest.mark.anyio()
async def test_not_authenticate_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    authenticated_user = await crud_user.authenticate(db, email, password)
    assert authenticated_user is None


@pytest.mark.anyio()
async def test_check_if_user_is_active(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    await crud_user.activate(db, user)
    assert user.is_active is True


@pytest.mark.anyio()
async def test_check_if_user_is_active_inactive(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    assert user.is_active is False


@pytest.mark.anyio()
async def test_check_if_user_is_superuser(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in, is_superuser=True)
    assert user.is_superuser is True


@pytest.mark.anyio()
async def test_check_if_user_is_superuser_normal_user(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    assert user.is_superuser is False


@pytest.mark.anyio()
async def test_get_user(db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = await crud_user.create(db, user_in)
    user_2 = await crud_user.get(db, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.anyio()
async def test_update_user(db: AsyncSession) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in, is_superuser=True)
    new_password = random_lower_string()
    user_in_update = UserUpdatePassword(password=new_password)
    await crud_user.update(db, user, user_in_update)
    user_2 = await crud_user.get(db, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
