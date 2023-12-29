from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import random_lower_string


async def test_create_item(
    client: AsyncClient, normal_user_token_headers: dict
) -> None:
    data = {"title": random_lower_string(), "description": random_lower_string()}
    response = await client.post(
        "/items/", headers=normal_user_token_headers, json=data
    )
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content.get("id")
    assert content.get("owner_id")


async def test_read_item(
    client: AsyncClient,
    normal_user_token_headers: dict,
    session: AsyncSession,
    normal_user: User,
) -> None:
    item = await create_random_item(session, normal_user.id)
    response = await client.get(f"/items/{item.id}", headers=normal_user_token_headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)
