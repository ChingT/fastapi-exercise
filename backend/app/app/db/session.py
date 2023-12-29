from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

if settings.ENVIRONMENT == "PYTEST":
    sqlalchemy_database_uri = settings.ASYNC_TEST_DATABASE_URI
else:
    sqlalchemy_database_uri = settings.ASYNC_DATABASE_URI


engine = create_async_engine(
    sqlalchemy_database_uri,
    echo=False,
    future=True,
    # Asincio pytest works with NullPool
    poolclass=NullPool if settings.ENVIRONMENT == "PYTEST" else QueuePool,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
