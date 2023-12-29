import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.item import crud_item
from app.models.item import ItemCreate, ItemUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


@pytest.mark.anyio()
async def test_create_item(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = await create_random_user(db)
    item = await crud_item.create_with_owner(db, item_in, user.id)
    assert item.title == title
    assert item.description == description
    assert item.owner.id == user.id


@pytest.mark.anyio()
async def test_get_item(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = await create_random_user(db)
    item = await crud_item.create_with_owner(db, item_in, user.id)
    stored_item = await crud_item.get(db, item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description
    assert item.owner.id == stored_item.owner_id


@pytest.mark.anyio()
async def test_update_item(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = await create_random_user(db)
    item = await crud_item.create_with_owner(db, item_in, user.id)
    description2 = random_lower_string()
    item_update = ItemUpdate(description=description2)
    item2 = await crud_item.update(db, item, item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2
    assert item.owner.id == item2.owner_id


@pytest.mark.anyio()
async def test_delete_item(db: AsyncSession) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    user = await create_random_user(db)
    item = await crud_item.create_with_owner(db, item_in, user.id)
    item2 = await crud_item.delete(db, item)
    item3 = await crud_item.get(db, item.id)
    assert item2 is None
    assert item3 is None
