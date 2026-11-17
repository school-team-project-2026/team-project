from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.services.candidate_similarity import find_similar_candidates


class FakeEmbeddingProvider:
    provider_name = "fake"
    model_name = "test-model"
    dimensions = 2

    def __init__(self) -> None:
        self.query_calls = 0

    def embed_query(self, text: str) -> list[float]:
        self.query_calls += 1
        return [1.0, 0.0]

    def embed_passage(self, text: str) -> list[float]:
        if "名称: オクトパストラベラーII" in text:
            return [1.0, 0.0]

        if "名称: パンデミック" in text:
            return [0.8, 0.6]

        if "名称: ボルダリング" in text:
            return [0.0, 1.0]

        raise AssertionError("Unexpected candidate")


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Candidate.__table__.create(engine)

    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()


def make_candidate(
    name: str,
    is_active: bool = True,
) -> Candidate:
    return Candidate(
        name=name,
        candidate_type="work",
        domain="game",
        genre=None,
        description="テスト用の候補です。",
        appeal_tags=["戦略性"],
        is_active=is_active,
    )


def test_candidates_are_sorted_by_similarity(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            make_candidate("ボルダリング"),
            make_candidate("パンデミック"),
            make_candidate("オクトパストラベラーII"),
            make_candidate("非公開候補", is_active=False),
        ]
    )
    db_session.commit()

    provider = FakeEmbeddingProvider()

    results = find_similar_candidates(
        session=db_session,
        embedding_provider=provider,
        query_text="戦略を考えるのが好き",
    )

    names = [item.candidate.name for item in results]

    assert names == [
        "オクトパストラベラーII",
        "パンデミック",
        "ボルダリング",
    ]
    assert results[0].similarity == pytest.approx(1.0)
    assert provider.query_calls == 1


def test_limit_is_applied(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            make_candidate("ボルダリング"),
            make_candidate("オクトパストラベラーII"),
        ]
    )
    db_session.commit()

    results = find_similar_candidates(
        session=db_session,
        embedding_provider=FakeEmbeddingProvider(),
        query_text="戦略性",
        limit=1,
    )

    assert len(results) == 1
    assert results[0].candidate.name == "オクトパストラベラーII"


def test_empty_database_returns_empty_list(
    db_session: Session,
) -> None:
    provider = FakeEmbeddingProvider()

    results = find_similar_candidates(
        session=db_session,
        embedding_provider=provider,
        query_text="戦略性",
    )

    assert results == []
    assert provider.query_calls == 0


def test_empty_query_is_rejected(
    db_session: Session,
) -> None:
    with pytest.raises(ValueError, match="Query text must not be empty"):
        find_similar_candidates(
            session=db_session,
            embedding_provider=FakeEmbeddingProvider(),
            query_text="   ",
        )
