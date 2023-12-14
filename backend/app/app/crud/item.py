from fastapi import Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Item
from app.schemas.item import ItemCreateRequest, ItemUpdateRequest


class CRUDItem(CRUDBase[Item, ItemCreateRequest, ItemUpdateRequest]):
    def create_with_owner(self, db: Session, *, obj_in: ItemCreateRequest) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Item(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def list_by_owner(
        self,
        db: Session,
        *,
        user_id: int,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
    ) -> list[Item]:
        return (
            db.query(Item)
            .filter(Item.owner_id == user_id)
            .offset(offset)
            .limit(limit)
            .all()
        )


crud_item = CRUDItem(Item)
