from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.models.user import User


async def test_get_access_token(client: AsyncClient, superuser: User) -> None:
    login_data = {
        "username": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD,
    }
    r = await client.post("/auth/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert tokens["access_token"]


async def test_use_access_token(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    r = await client.post("/auth/test-token", headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert "email" in result
