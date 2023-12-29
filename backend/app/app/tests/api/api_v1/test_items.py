import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.tests.utils.item import create_random_item


@pytest.mark.anyio()
async def test_create_item(client: AsyncClient, superuser_token_headers: dict) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = await client.post("/items/", headers=superuser_token_headers, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content.get("id")
    assert content.get("owner_id")


@pytest.mark.anyio()
async def test_read_item(
    client: AsyncClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    item = await create_random_item(db)
    response = await client.get(f"/items/{item.id}", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)
