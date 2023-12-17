from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, SessionDep
from app.api.utils import item_not_found_exception, no_permissions_exception
from app.crud.item import crud_item
from app.models.item import ItemCreate, ItemOut, ItemUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    db: SessionDep, item: ItemCreate, current_user: CurrentUser
) -> ItemOut:
    obj_in = {**item.model_dump(), "owner_id": current_user.id}
    return crud_item.create_with_owner(db, obj_in=obj_in)


@router.get("/")
def read_items(
    db: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[ItemOut]:
    """Retrieve items. The user can only retrieve their own items."""
    if current_user.is_superuser:
        return crud_item.list(db, offset=offset, limit=limit)
    return crud_item.list_by_owner(
        db, user_id=current_user.id, offset=offset, limit=limit
    )


@router.get("/{item_id}")
def read_item(db: SessionDep, current_user: CurrentUser, item_id: UUID) -> ItemOut:
    """Retrieve item by ID. The user can only retrieve their own item."""
    item = crud_item.get(db, id=item_id)
    if not item:
        raise item_not_found_exception
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise no_permissions_exception
    return item


@router.put("/{item_id}")
def update_item(
    db: SessionDep, current_user: CurrentUser, item_id: UUID, item_in: ItemUpdate
) -> ItemOut:
    """Update an item."""
    item = crud_item.get(db, id=item_id)
    if not item:
        raise item_not_found_exception
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise no_permissions_exception

    return crud_item.update(db, db_obj=item, obj_in=item_in)


@router.delete("/{item_id}")
def delete_item(db: SessionDep, current_user: CurrentUser, item_id: UUID) -> ItemOut:
    """Delete an item."""
    item = crud_item.get(db, id=item_id)
    if not item:
        raise item_not_found_exception
    if not current_user.is_superuser and item.owner_id != current_user.id:
        raise no_permissions_exception
    return crud_item.delete(db, id=item_id)
