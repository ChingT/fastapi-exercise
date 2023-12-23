from uuid import UUID

from fastapi import Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.utils import item_not_found_exception, no_permissions_exception
from app.crud.base import CRUDBase
from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.user import User


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def create_with_owner(
        self, session: AsyncSession, obj_in: ItemCreate, user_id: UUID
    ) -> Item:
        db_obj = Item.model_validate(obj_in.model_dump(), update={"owner_id": user_id})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def list_by_owner(
        self,
        session: AsyncSession,
        user_id: UUID,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
    ) -> list[Item]:
        query = (
            select(self.model)
            .filter(Item.owner_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        result = await session.exec(query)
        return result.all()

    async def get_by_owner(
        self, session: AsyncSession, id: UUID, user: User
    ) -> Item | None:
        db_obj = await self.get(session, id)
        if not db_obj:
            raise item_not_found_exception
        if not user.is_superuser and db_obj.owner_id != user.id:
            raise no_permissions_exception
        return db_obj


crud_item = CRUDItem(Item)
