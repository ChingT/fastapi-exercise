from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .base_uuid_model import BaseUUIDModel
from .user import User, UserOut


class ItemBase(SQLModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = None


class Item(BaseUUIDModel, ItemBase, table=True):
    title: str
    owner_id: UUID | None = Field(default=None, foreign_key="user.id")
    owner: User | None = Relationship(back_populates="items")


class ItemOut(ItemBase):
    id: UUID
    updated_at: datetime
    created_at: datetime
    owner: UserOut
