from typing import TYPE_CHECKING

from pydantic import EmailStr, computed_field
from sqlmodel import Column, Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from .item import Item


class UserBase(SQLModel):
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_active: bool = True
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


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


class UserOut(UserBase):
    id: int

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
