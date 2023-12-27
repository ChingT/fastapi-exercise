from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.user import crud_user
from app.models.user import User, UserCreate, UserUpdatePassword
from app.tests.utils.utils import random_email, random_lower_string


def get_user_authentication_headers(
    client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"email": email, "password": password}
    r = client.post("/auth/access-token", data=data)
    response = r.json()
    return {"Authorization": f"Bearer {response['access_token']}"}


def get_superuser_authentication_headers(client: TestClient) -> dict[str, str]:
    data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/auth/access-token", data=data)
    response = r.json()
    return {"Authorization": f"Bearer {response['access_token']}"}


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    return crud_user.create(db, user_in)


def get_authentication_token_from_email(
    db: Session, client: TestClient, email: str
) -> dict[str, str]:
    """Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud_user.get_by_email(db, email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = crud_user.create(db, user_in_create)
    else:
        user_in_update = UserUpdatePassword(password=password)
        user = crud_user.update(db, user, user_in_update)

    return get_user_authentication_headers(client, email, password)
