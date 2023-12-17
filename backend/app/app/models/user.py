from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr, computed_field
from sqlmodel import Column, Field, Relationship, SQLModel, String

from .base_uuid_model import BaseUUIDModel

if TYPE_CHECKING:
    from .item import Item


class UserBase(SQLModel):
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_active: bool = False
    is_superuser: bool = False
    first_name: str | None = None
    last_name: str | None = None

    def __str__(self):
        return f"User {self.email}"


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None


class UserUpdatePassword(SQLModel):
    password: str


class UserRecoverPassword(SQLModel):
    email: EmailStr


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str
    items: list["Item"] = Relationship(
        back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class UserOut(UserBase):
    id: UUID

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
