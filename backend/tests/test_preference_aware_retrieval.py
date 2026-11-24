from collections.abc import Iterator
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.ai.preference_extractor import PreferenceExtractor
from app.ai.schemas import NegativePreference, PreferenceFeatures
from app.models.candidate import Candidate
from app.schemas.recommendation import RecommendationRequest
from app.services.preference_aware_retrieval import (
    PreferenceExtractionError,
    retrieve_preference_aware_candidates,
)


class FakePreferenceProvider:
    provider_name = "fake"
    model_name = "fake-preference-model"

    def __init__(
        self,
        result: PreferenceFeatures | Exception,
    ) -> None:
        self.result = result
        self.calls: list[tuple[str, str, str]] = []

    def extract(
        self,
        *,
        name: str,
        category: str,
        comment: str,
    ) -> PreferenceFeatures:
        self.calls.append((name, category, comment))

        if isinstance(self.result, Exception):
            raise self.result

        return self.result


class FakeEmbeddingProvider:
    provider_name = "fake"
    model_name = "fake-embedding-model"
    dimensions = 2

    def __init__(self) -> None:
        self.query_texts: list[str] = []

    def embed_query(self, text: str) -> list[float]:
        self.query_texts.append(text)

        if "攻略" in text:
            return [1.0, 0.0]

        return [0.0, 1.0]

    def embed_passage(self, text: str) -> list[float]:
        if "名称: オクトパストラベラーII" in text:
            return [1.0, 0.0]

        if "名称: ボルダリング" in text:
            return [0.0, 1.0]

        raise AssertionError("Unexpected candidate")


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")

    Candidate.__table__.create(engine)

    try:
        with Session(engine) as session:
            session.add_all(
                [
                    Candidate(
                        name="オクトパストラベラーII",
                        candidate_type="work",
                        domain="game",
                        genre="turn_based_rpg",
                        description="戦略的なターン制RPG。",
                        appeal_tags=["戦略性", "弱点分析"],
                        is_active=True,
                    ),
                    Candidate(
                        name="ボルダリング",
                        candidate_type="activity",
                        domain="sports",
                        genre=None,
                        description="登るルートを考えるスポーツ。",
                        appeal_tags=["課題攻略"],
                        is_active=True,
                    ),
                ]
            )
            session.commit()
            yield session
    finally:
        engine.dispose()


def make_features(
    appeal_points: list[str],
) -> PreferenceFeatures:
    return PreferenceFeatures(
        attributes=[],
        appeal_points=appeal_points,
        desired_experiences=[],
        values=[],
        keywords=[],
        negative_preferences=[],
    )


def test_uses_extracted_features_when_reason_exists(
    db_session: Session,
) -> None:
    provider = FakePreferenceProvider(make_features(["攻略法の発見"]))
    embedding = FakeEmbeddingProvider()

    result = retrieve_preference_aware_candidates(
        session=db_session,
        request=RecommendationRequest(
            interest_text="ターン制RPG",
            liked_aspects="強敵の攻略法を考えるのが好き",
        ),
        extractor=PreferenceExtractor(provider),
        embedding_provider_factory=lambda: embedding,
    )

    assert result.search_method == "extracted"
    assert result.features is not None
    assert result.query_text == "魅力: 攻略法の発見"
    assert embedding.query_texts == [result.query_text]

    assert provider.calls == [
        (
            "ターン制RPG",
            "未指定",
            "強敵の攻略法を考えるのが好き",
        )
    ]

    assert result.candidates[0].candidate.name == ("オクトパストラベラーII")


def test_uses_raw_query_without_reason(
    db_session: Session,
) -> None:
    provider = FakePreferenceProvider(make_features(["攻略法の発見"]))
    embedding = FakeEmbeddingProvider()

    result = retrieve_preference_aware_candidates(
        session=db_session,
        request=RecommendationRequest(
            interest_text="ターン制RPG",
        ),
        extractor=PreferenceExtractor(provider),
        embedding_provider_factory=lambda: embedding,
    )

    assert result.search_method == "raw"
    assert result.query_text == "ターン制RPG"
    assert result.features is None
    assert provider.calls == []
    assert embedding.query_texts == ["ターン制RPG"]


def test_falls_back_when_extracted_features_are_empty(
    db_session: Session,
) -> None:
    provider = FakePreferenceProvider(make_features([]))
    embedding = FakeEmbeddingProvider()

    result = retrieve_preference_aware_candidates(
        session=db_session,
        request=RecommendationRequest(
            interest_text="ターン制RPG",
            liked_aspects="楽しいから",
        ),
        extractor=PreferenceExtractor(provider),
        embedding_provider_factory=lambda: embedding,
    )

    expected_query = "ターン制RPG"

    assert result.query_text == expected_query
    assert embedding.query_texts == [expected_query]
    assert result.search_method == "raw"
    assert result.features == make_features([])
    assert len(provider.calls) == 1


def test_stops_before_search_when_extraction_fails(
    db_session: Session,
) -> None:
    provider = FakePreferenceProvider(RuntimeError("Simulated AI failure"))
    embedding = FakeEmbeddingProvider()

    request = RecommendationRequest(
        interest_text="ターン制RPG",
        liked_aspects="攻略を考えるのが好き",
    )

    with patch(
        "app.services.preference_aware_retrieval.find_similar_candidates"
    ) as mock_search:
        with pytest.raises(PreferenceExtractionError):
            retrieve_preference_aware_candidates(
                session=db_session,
                request=request,
                extractor=PreferenceExtractor(provider),
                embedding_provider_factory=lambda: embedding,
            )

        mock_search.assert_not_called()


def test_uses_interest_only_when_only_negative_preferences_exist(
    db_session: Session,
) -> None:
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

    provider = FakePreferenceProvider(extracted)
    embedding = FakeEmbeddingProvider()

    result = retrieve_preference_aware_candidates(
        session=db_session,
        request=RecommendationRequest(
            interest_text="ターン制RPG",
            liked_aspects="高い場所は絶対に避けたい",
        ),
        extractor=PreferenceExtractor(provider),
        embedding_provider_factory=lambda: embedding,
    )

    # 非希望の文章をEmbeddingに混入させない。
    assert result.query_text == "ターン制RPG"
    assert embedding.query_texts == ["ターン制RPG"]
    assert result.search_method == "raw"

    # 抽出に成功したNegative Preferenceは保持する。
    assert result.features is not None
    assert result.features == extracted
    assert result.features.negative_preferences == (extracted.negative_preferences)
