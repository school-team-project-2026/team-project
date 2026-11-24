from unittest.mock import patch as mock_patch

import pytest
from fastapi.testclient import TestClient

from app.ai.schemas import NegativePreference, PreferenceFeatures
from app.main import app
from app.models.candidate import Candidate
from app.routers.recommendations import (
    get_embedding_provider_factory,
    get_extractor,
    get_session,
)


def make_candidate(
    candidate_id: int,
    name: str,
    domain: str,
    modes: list[str],
) -> Candidate:
    return Candidate(
        id=candidate_id,
        name=name,
        candidate_type="activity",
        domain=domain,
        genre=None,
        description=f"{name}のテスト用説明",
        appeal_tags=["テスト用の魅力"],
        interaction_modes=modes,
    )


CANDIDATES = [
    make_candidate(16, "ジャズ鑑賞", "music", ["listen"]),
    make_candidate(17, "バンドでの合奏", "music", ["perform"]),
    make_candidate(7, "ボルダリング", "sports", ["participate"]),
    make_candidate(15, "お菓子作り", "cooking", ["create"]),
    make_candidate(22, "インターステラー", "movie", ["watch"]),
    make_candidate(20, "三体", "book", ["read"]),
]


class FakeSession:
    def scalars(self, statement):
        class Result:
            def all(self):
                return CANDIDATES

        return Result()


class FakeExtractor:
    def extract(self, *, name, category, comment):
        return PreferenceFeatures(
            attributes=["速いテンポ"],
            appeal_points=["楽器の掛け合い"],
            desired_experiences=["音楽を聴く"],
            values=[],
            keywords=["ジャズ"],
            negative_preferences=[
                NegativePreference(
                    target="自分で演奏すること",
                    strength="low_interest",
                    evidence=("自分で演奏することには特に興味はありません"),
                )
            ],
        )


class FailingExtractor:
    def extract(self, *, name, category, comment):
        raise RuntimeError("Simulated extraction failure")


class FakeEmbeddingProvider:
    provider_name = "fake"
    model_name = "fake-model"
    dimensions = 2

    def embed_query(self, text):
        return [1.0, 0.0]

    def embed_passage(self, text):
        if "バンドでの合奏" in text:
            return [1.0, 0.0]
        if "ジャズ鑑賞" in text:
            return [0.95, 0.05]
        return [0.8, 0.2]


@pytest.fixture
def embedding_provider_factory():
    with mock_patch(
        "app.routers.recommendations.get_embedding_provider",
        side_effect=FakeEmbeddingProvider,
    ) as factory:
        yield factory


@pytest.fixture
def client(embedding_provider_factory):
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_session] = lambda: FakeSession()
    app.dependency_overrides[get_extractor] = lambda: FakeExtractor()

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)


def test_recommendations_apply_negative_preferences(client):
    response = client.post(
        "/recommendations",
        json={
            "interest_text": "ジャズ",
            "liked_aspects": (
                "速い演奏を聴くのが好きです。"
                "自分で演奏することには特に興味はありません。"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()
    items = body["recommendations"]
    names = [item["name"] for item in items]

    assert body["analysis"]["basis"] == "user_comment"
    assert len(items) == 5
    assert "ジャズ鑑賞" in names
    assert "バンドでの合奏" not in names
    assert all("【サンプル】" not in item["reason"] for item in items)

    # 現行の推薦タイプを検証する。
    assert all(
        item["recommendation_type"] in {"same_genre", "cross_genre"} for item in items
    )

    # 同系統・異分野の分類を検証する。
    types_by_name = {item["name"]: item["recommendation_type"] for item in items}

    assert types_by_name["ジャズ鑑賞"] == "same_genre"
    assert types_by_name["インターステラー"] == "cross_genre"

    # 同一Candidateが重複していないことを検証する。
    assert len({item["candidate_id"] for item in items}) == len(items)


@pytest.mark.parametrize(
    "payload",
    [
        {"interest_text": "ジャズ"},
        {"interest_text": "ジャズ", "liked_aspects": "   "},
    ],
)
def test_recommendations_without_liked_aspects(
    client, payload, embedding_provider_factory
):
    # このテストだけ本物のget_extractorを使用する。
    app.dependency_overrides.pop(get_extractor, None)

    # Groqの生成処理が呼ばれたら、テストを失敗させる。
    with mock_patch(
        "app.routers.recommendations.get_cached_extractor",
        side_effect=AssertionError("Groq must not be initialized"),
    ) as mock_factory:
        response = client.post(
            "/recommendations",
            json=payload,
        )

    assert response.status_code == 200

    body = response.json()
    assert body["analysis"]["basis"] == "general_characteristics"
    assert len(body["recommendations"]) == 5

    mock_factory.assert_not_called()
    embedding_provider_factory.assert_called_once_with()


def test_extraction_failure_returns_503(client):
    app.dependency_overrides[get_extractor] = lambda: FailingExtractor()
    app.dependency_overrides.pop(get_embedding_provider_factory, None)

    with (
        mock_patch(
            "app.routers.recommendations.get_embedding_provider",
            side_effect=RuntimeError("E5 initialization failed"),
        ) as mock_embedding,
        mock_patch(
            "app.services.preference_aware_retrieval.find_similar_candidates"
        ) as mock_search,
    ):
        response = client.post(
            "/recommendations",
            json={
                "interest_text": "ジャズ",
                "liked_aspects": "演奏には興味がありません",
            },
        )

    assert response.status_code == 503
    mock_embedding.assert_not_called()
    mock_search.assert_not_called()


@pytest.mark.parametrize(
    "payload",
    [
        {"interest_text": ""},
        {"interest_text": "   ", "liked_aspects": None},
    ],
)
def test_empty_interest_is_rejected(client, payload):
    app.dependency_overrides.pop(get_embedding_provider_factory, None)

    with mock_patch(
        "app.routers.recommendations.get_embedding_provider",
        side_effect=RuntimeError("E5 initialization failed"),
    ) as mock_embedding:
        response = client.post(
            "/recommendations",
            json=payload,
        )

    assert response.status_code == 422
    mock_embedding.assert_not_called()


def test_groq_initialization_failure_returns_503(client, embedding_provider_factory):
    # FakeExtractorのoverrideを外す。
    app.dependency_overrides.pop(get_extractor, None)

    with mock_patch(
        "app.routers.recommendations.get_cached_extractor",
        side_effect=RuntimeError("Groq initialization failed"),
    ) as mock_factory:
        response = client.post(
            "/recommendations",
            json={
                "interest_text": "ジャズ",
                "liked_aspects": "楽器の掛け合いが好き",
            },
        )

    assert response.status_code == 503
    mock_factory.assert_called_once_with()
    embedding_provider_factory.assert_not_called()


def test_embedding_initialization_failure_returns_503(client):
    app.dependency_overrides.pop(
        get_embedding_provider_factory,
        None,
    )

    with (
        mock_patch(
            "app.routers.recommendations.get_embedding_provider",
            side_effect=RuntimeError("E5 initialization failed"),
        ) as mock_embedding,
        mock_patch(
            "app.services.preference_aware_retrieval.find_similar_candidates"
        ) as mock_search,
    ):
        response = client.post(
            "/recommendations",
            json={
                "interest_text": "ジャズ",
                "liked_aspects": "楽器の掛け合いが好き",
            },
        )

    assert response.status_code == 503
    assert response.json() == {
        "detail": ("推薦モデルを利用できません。時間をおいて再度お試しください。"),
    }

    mock_embedding.assert_called_once_with()
    mock_search.assert_not_called()


def test_recommendations_can_return_empty_results(client):
    extracted = PreferenceFeatures(
        attributes=[],
        appeal_points=[],
        desired_experiences=[],
        values=[],
        keywords=[],
        negative_preferences=[
            NegativePreference(
                target="高い場所",
                strength="avoid",
                evidence="高い場所は絶対に避けたい",
            )
        ],
    )

    with mock_patch.object(
        FakeExtractor,
        "extract",
        return_value=extracted,
    ):
        response = client.post(
            "/recommendations",
            json={
                "interest_text": "ジャズ",
                "liked_aspects": "高い場所は絶対に避けたい",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["recommendations"] == []
    assert body["analysis"]["basis"] == "user_comment"


def test_recommendations_openapi_contract(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    operation = schema["paths"]["/recommendations"]["post"]

    responses = operation["responses"]

    assert "200" in responses
    assert "422" in responses
    assert "503" in responses

    schemas = schema["components"]["schemas"]

    error_schema = schemas["RecommendationUnavailableResponse"]
    assert error_schema["properties"]["detail"]["type"] == "string"

    recommendation_schema = schemas["RecommendationResponse"]
    items_schema = recommendation_schema["properties"]["recommendations"]

    assert items_schema["maxItems"] == 5
