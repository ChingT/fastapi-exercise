from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.item import create_random_item


def test_create_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post("/items/", headers=superuser_token_headers, json=data)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(f"/items/{item.id}", headers=superuser_token_headers)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
