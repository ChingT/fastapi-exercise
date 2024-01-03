import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.main import app
from app.models import *  # noqa: F403
from app.models.user import User
from app.tests.utils.user import create_test_user, get_user_authentication_headers

target_metadata = SQLModel.metadata


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def testdb_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert settings.ENVIRONMENT == "PYTEST"

    # always drop and create test db tables between tests session
    async with engine.begin() as conn:
        await conn.run_sync(target_metadata.drop_all)
        await conn.run_sync(target_metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(testdb_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

        # delete all data from all tables after test
        for table in target_metadata.sorted_tables[::-1]:
            await session.exec(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture()
async def superuser(testdb_setup_sessionmaker, session: AsyncSession) -> User:
    return await create_test_user(session, is_superuser=True)


@pytest_asyncio.fixture()
async def normal_user(testdb_setup_sessionmaker, session: AsyncSession) -> User:
    return await create_test_user(session, is_superuser=False)


@pytest_asyncio.fixture()
async def superuser_token_headers(superuser: User) -> dict[str, str]:
    return await get_user_authentication_headers(superuser)


@pytest_asyncio.fixture()
async def normal_user_token_headers(normal_user: User) -> dict[str, str]:
    return await get_user_authentication_headers(normal_user)
