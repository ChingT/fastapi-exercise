import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud.user import crud_user
from app.models.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.anyio()
async def test_get_users_superuser_me(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    r = await client.get("/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


@pytest.mark.anyio()
async def test_get_users_normal_user_me(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = await client.get("/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


@pytest.mark.anyio()
async def test_create_user_new_email(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = await client.post("/users/", headers=superuser_token_headers, json=data)
    assert status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    created_user = r.json()
    user = await crud_user.get_by_email(db, email)
    assert user
    assert user.email == created_user["email"]


@pytest.mark.anyio()
async def test_get_existing_user(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = await crud_user.create(db, user_in)
    user_id = user.id
    r = await client.get(f"/users/{user_id}", headers=superuser_token_headers)
    assert status.HTTP_200_OK <= r.status_code < status.HTTP_300_MULTIPLE_CHOICES
    api_user = r.json()
    existing_user = await crud_user.get_by_email(db, email=email)
    assert existing_user
    assert existing_user.email == api_user["email"]


@pytest.mark.anyio()
async def test_create_user_existing_username(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    await crud_user.create(db, user_in)
    data = {"email": email, "password": password}
    r = await client.post("/users/", headers=superuser_token_headers, json=data)
    created_user = r.json()
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "_id" not in created_user


@pytest.mark.anyio()
async def test_create_user_by_normal_user(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = await client.post("/users/", headers=normal_user_token_headers, json=data)
    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio()
async def test_retrieve_users(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    await crud_user.create(db, user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    await crud_user.create(db, user_in2)

    r = await client.get("/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
