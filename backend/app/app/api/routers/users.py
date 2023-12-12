from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, SessionDep, get_current_superuser
from app.crud.user import crud_user
from app.schemas.user import (
    UserCreateRequest,
    UserResponse,
    UserUpdatePasswordRequest,
    UserUpdateRequest,
)

router = APIRouter()


@router.get("/me")
def read_current_user(current_user: CurrentUser) -> UserResponse:
    """Get current user."""
    return current_user


@router.put("/me")
def update_current_user(
    db: SessionDep, current_user: CurrentUser, updated_data: UserUpdateRequest
) -> UserResponse:
    """Update current user."""
    return crud_user.update(db, db_obj=current_user, obj_in=updated_data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(db: SessionDep, current_user: CurrentUser):
    """Delete current user."""
    crud_user.delete(db, id=current_user.id)


@router.post(
    "/",
    dependencies=[Depends(get_current_superuser)],
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(db: SessionDep, user: UserCreateRequest) -> UserResponse:
    if crud_user.get_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create(db, obj_in=user)


@router.get("/", dependencies=[Depends(get_current_superuser)])
def read_users(db: SessionDep, skip: int = 0, limit: int = 100) -> list[UserResponse]:
    return crud_user.list(db, skip=skip, limit=limit)


@router.get("/{user_id}", dependencies=[Depends(get_current_superuser)])
def read_user(db: SessionDep, user_id: int) -> UserResponse:
    db_obj = crud_user.get(db, id=user_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_obj


@router.post("/reset-password", status_code=status.HTTP_201_CREATED)
async def reset_current_user_password(
    db: SessionDep,
    current_user: CurrentUser,
    updated_password: UserUpdatePasswordRequest,
) -> UserResponse:
    """Update current user password."""
    return crud_user.update(db, db_obj=current_user, obj_in=updated_password)
