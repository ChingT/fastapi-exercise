from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.item import crud_item
from app.models.item import ItemCreate, ItemUpdate
from app.models.user import User
from app.tests.utils.utils import random_lower_string


async def test_create_item(session: AsyncSession, normal_user: User) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = await crud_item.create_with_owner(session, item_in, normal_user.id)
    assert item.title == title
    assert item.description == description
    assert item.owner.id == normal_user.id


async def test_get_item(session: AsyncSession, normal_user: User) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = await crud_item.create_with_owner(session, item_in, normal_user.id)
    stored_item = await crud_item.get(session, item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description
    assert item.owner.id == stored_item.owner_id


async def test_update_item(session: AsyncSession, normal_user: User) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = await crud_item.create_with_owner(session, item_in, normal_user.id)
    description2 = random_lower_string()
    item_update = ItemUpdate(description=description2)
    item2 = await crud_item.update(session, item, item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2
    assert item.owner.id == item2.owner_id


async def test_delete_item(session: AsyncSession, normal_user: User) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item = await crud_item.create_with_owner(session, item_in, normal_user.id)
    item2 = await crud_item.delete(session, item)
    item3 = await crud_item.get(session, item.id)
    assert item2 is None
    assert item3 is None
