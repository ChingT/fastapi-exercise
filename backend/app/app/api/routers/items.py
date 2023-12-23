from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, SessionDep
from app.crud.item import crud_item
from app.models.item import ItemCreate, ItemOut, ItemUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item_for_user(
    session: SessionDep, item: ItemCreate, current_user: CurrentUser
) -> ItemOut:
    return await crud_item.create_with_owner(session, item, current_user.id)


@router.get("/")
async def read_items(
    session: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[ItemOut]:
    """Retrieve items. The user can only retrieve their own items."""
    if current_user.is_superuser:
        return await crud_item.list(session, offset, limit)
    return await crud_item.list_by_owner(session, current_user.id, offset, limit)


@router.get("/{item_id}")
async def read_item(
    session: SessionDep, current_user: CurrentUser, item_id: UUID
) -> ItemOut:
    """Retrieve item by ID. The user can only retrieve their own item."""
    return await crud_item.get_by_owner(session, item_id, current_user)


@router.patch("/{item_id}")
async def update_item(
    session: SessionDep, current_user: CurrentUser, item_id: UUID, item_in: ItemUpdate
) -> ItemOut:
    """Update an item."""
    item = await crud_item.get_by_owner(session, item_id, current_user)
    return await crud_item.update(session, item, item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(session: SessionDep, current_user: CurrentUser, item_id: UUID):
    """Delete an item."""
    item = await crud_item.get_by_owner(session, item_id, current_user)
    await crud_item.delete(session, item)
    return {"msg": "Item deleted"}
