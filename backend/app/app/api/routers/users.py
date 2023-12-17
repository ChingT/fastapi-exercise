from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_user,
    get_current_superuser,
)
from app.api.utils import email_registered_exception, user_not_found_exception
from app.crud.user import crud_user
from app.models.user import UserCreate, UserOut, UserUpdate

router = APIRouter()


@router.get("/me")
def read_current_user(current_user: CurrentUser) -> UserOut:
    """Get current user."""
    return current_user


@router.put("/me")
def update_current_user(
    db: SessionDep, current_user: CurrentUser, updated_data: UserUpdate
) -> UserOut:
    """Update current user."""
    return crud_user.update(db, db_obj=current_user, obj_in=updated_data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(db: SessionDep, current_user: CurrentUser):
    """Delete current user."""
    crud_user.delete(db, id=current_user.id)
    return current_user


@router.post(
    "/",
    dependencies=[Depends(get_current_superuser)],
    status_code=status.HTTP_201_CREATED,
)
def create_user(db: SessionDep, user: UserCreate) -> UserOut:
    """Only superuser can perform this operation."""
    if crud_user.get_by_email(db, email=user.email):
        raise email_registered_exception
    return crud_user.create(db, obj_in=user)


@router.get("/", dependencies=[Depends(get_current_active_user)])
def read_users(
    db: SessionDep, offset: int = 0, limit: int = Query(default=100, le=100)
) -> list[UserOut]:
    return crud_user.list(db, offset=offset, limit=limit)


@router.get("/{user_id}", dependencies=[Depends(get_current_active_user)])
def read_user(db: SessionDep, user_id: UUID) -> UserOut:
    db_obj = crud_user.get(db, id=user_id)
    if db_obj is None:
        raise user_not_found_exception
    return db_obj
