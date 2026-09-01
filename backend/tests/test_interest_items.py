from fastapi.testclient import TestClient


def test_create_and_list_interest_items(client: TestClient) -> None:
    payload = {
        "name": "ブルーアーカイブ",
        "category": "game",
        "comment": "世界観とキャラクター同士の関係性が好き",
    }

    create_response = client.post(
        "/interest-items",
        json=payload,
    )

    assert create_response.status_code == 201

    created_item = create_response.json()

    assert created_item["name"] == payload["name"]
    assert created_item["category"] == payload["category"]
    assert created_item["comment"] == payload["comment"]
    assert isinstance(created_item["id"], int)
    assert created_item["created_at"] is not None

    list_response = client.get("/interest-items")

    assert list_response.status_code == 200

    items = list_response.json()

    assert len(items) == 1
    assert items[0]["id"] == created_item["id"]
    assert items[0]["name"] == payload["name"]
