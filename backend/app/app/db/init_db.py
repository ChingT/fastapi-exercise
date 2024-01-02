import asyncio
import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud.user import crud_user
from app.db.session import SessionLocal
from app.models.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    async with SessionLocal() as session:
        await create_superuser(session)


async def create_superuser(session: AsyncSession) -> None:
    if user := await crud_user.get_by_email(session, settings.FIRST_SUPERUSER_EMAIL):
        logging.info("Superuser %s exists in database", user)
        return

    new_user = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL, password=settings.FIRST_SUPERUSER_PASSWORD
    )
    user = await crud_user.create(session, new_user, is_superuser=True)
    await crud_user.activate(session, user)
    logging.info("Superuser %s created", user)


if __name__ == "__main__":
    asyncio.run(main())
