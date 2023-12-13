from pydantic import BaseModel, ConfigDict, EmailStr, computed_field

from app.schemas.item import ItemResponse


# Shared properties
class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None

    @computed_field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserCreateRequest(UserBase):
    email: EmailStr
    password: str


class UserUpdateRequest(UserBase):
    pass


class UserUpdatePasswordRequest(BaseModel):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool = False
    items: list[ItemResponse]
