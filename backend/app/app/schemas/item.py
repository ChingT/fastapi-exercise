from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    title: str | None = None
    description: str | None = None


class ItemCreateRequest(ItemBase):
    title: str


class ItemUpdateRequest(ItemBase):
    pass


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
