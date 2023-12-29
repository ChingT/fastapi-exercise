import asyncio
import logging

from sqlmodel import select

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    # Try to create session to check if DB is awake
    async with SessionLocal() as session:
        await session.exec(select(1))


async def main() -> None:
    logger.info("Initializing service")
    await init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    asyncio.run(main())
