from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommendations_with_reason():
    response = client.post(
        "/recommendations",
        json={
            "interest_text": "ターン制RPG",
            "liked_aspects": "戦略を考えて強敵を倒すのが好き",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["analysis"]["basis"] == "user_comment"
    assert len(data["recommendations"]) == 5

    types = [item["recommendation_type"] for item in data["recommendations"]]

    assert types.count("same_genre") == 1
    assert types.count("cross_genre") == 3
    assert types.count("adventure") == 1


def test_recommendations_without_reason():
    response = client.post(
        "/recommendations",
        json={
            "interest_text": "ターン制RPG",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["analysis"]["basis"] == "general_characteristics"
    assert len(data["recommendations"]) == 5


def test_recommendations_invalid_input():
    response = client.post(
        "/recommendations",
        json={
            "interest_text": "   ",
            "liked_aspects": None,
        },
    )

    assert response.status_code == 422
