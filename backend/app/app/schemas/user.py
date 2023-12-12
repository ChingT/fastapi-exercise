from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.item import ItemResponse


# Shared properties
class UserBase(BaseModel):
    is_superuser: bool = False


class UserCreateRequest(UserBase):
    email: EmailStr
    password: str


class UserUpdateRequest(UserBase):
    first_name: str | None = None
    last_name: str | None = None


class UserUpdatePasswordRequest(BaseModel):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    items: list[ItemResponse]
