from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.ai.preference_extractor import PreferenceExtractor
from app.ai.schemas import PreferenceFeatures
from app.models.candidate import Candidate
from app.schemas.recommendation import RecommendationRequest
from app.services.preference_aware_retrieval import (
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
        embedding_provider=embedding,
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
        embedding_provider=embedding,
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
        embedding_provider=embedding,
    )

    expected_query = "興味: ターン制RPG\n好きな理由: 楽しいから"

    assert result.query_text == expected_query
    assert embedding.query_texts == [expected_query]
    assert result.search_method == "raw"
    assert result.features is None
    assert len(provider.calls) == 1


def test_falls_back_when_extraction_fails(
    db_session: Session,
    caplog: pytest.LogCaptureFixture,
) -> None:
    provider = FakePreferenceProvider(RuntimeError("Simulated AI failure"))
    embedding = FakeEmbeddingProvider()

    result = retrieve_preference_aware_candidates(
        session=db_session,
        request=RecommendationRequest(
            interest_text="ターン制RPG",
            liked_aspects="攻略を考えるのが好き",
        ),
        extractor=PreferenceExtractor(provider),
        embedding_provider=embedding,
    )

    expected_query = (
    "興味: ターン制RPG\n"
    "好きな理由: 攻略を考えるのが好き"
    )

    assert result.search_method == "raw"
    assert result.query_text == expected_query
    assert result.features is None
    assert len(result.candidates) == 2
    assert embedding.query_texts == [expected_query]

    assert "Preference extraction failed" in caplog.text
