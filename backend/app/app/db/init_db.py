from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import crud_user
from app.models import User
from app.schemas.user import UserCreateRequest


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the line Base.metadata.create_all(bind=engine)

    user = session.execute(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if user:
        print("Superuser already exists in database")
        return

    new_user = UserCreateRequest(
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    user = crud_user.create(db=session, obj_in=new_user)
    print("Superuser was created")
