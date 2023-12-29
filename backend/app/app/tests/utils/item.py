from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.item import crud_item
from app.models.item import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_item(db: AsyncSession, owner_id: UUID | None = None) -> Item:
    if owner_id is None:
        user = await create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return await crud_item.create_with_owner(db, item_in, owner_id)
