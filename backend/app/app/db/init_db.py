import logging

from app.core.config import settings
from app.crud.user import crud_user
from app.db.database import SessionLocal
from app.models.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the line Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if user := crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL):
        logging.info("Superuser %s exists in database", user)
        return

    new_user = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL, password=settings.FIRST_SUPERUSER_PASSWORD
    )
    user = crud_user.create(db=db, obj_in=new_user, is_superuser=True)
    logging.info("Superuser %s created", user)


if __name__ == "__main__":
    main()
