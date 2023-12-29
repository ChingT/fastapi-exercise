from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app
from app.tests.utils.user import (
    get_authentication_token_from_email,
    get_superuser_authentication_headers,
)


@pytest.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


url = "http://localhost:8000"


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=url) as client:
        yield client


@pytest.fixture()
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_authentication_headers(client)


@pytest.fixture()
async def normal_user_token_headers(
    client: AsyncClient, db: AsyncSession
) -> dict[str, str]:
    return await get_authentication_token_from_email(
        db, client, settings.EMAIL_TEST_USER
    )
