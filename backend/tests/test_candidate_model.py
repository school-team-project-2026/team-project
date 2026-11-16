from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import Candidate


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")

    Candidate.__table__.create(engine)

    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()


def test_candidate_can_be_created_and_retrieved(
    db_session: Session,
) -> None:
    candidate = Candidate(
        name="オクトパストラベラーII",
        candidate_type="work",
        domain="game",
        genre="turn_based_rpg",
        description="戦略性を特徴とするターン制RPG。",
        appeal_tags=["戦略性", "弱点分析"],
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.expunge_all()

    saved = db_session.scalar(
        select(Candidate).where(Candidate.name == "オクトパストラベラーII")
    )

    assert saved is not None
    assert saved.id is not None
    assert saved.domain == "game"
    assert saved.appeal_tags == ["戦略性", "弱点分析"]


def test_candidate_genre_can_be_null(
    db_session: Session,
) -> None:
    candidate = Candidate(
        name="ボルダリング",
        candidate_type="activity",
        domain="sports",
        genre=None,
        description="課題の完登を目指すスポーツ。",
        appeal_tags=["試行錯誤"],
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    assert candidate.genre is None


def test_candidate_default_values(
    db_session: Session,
) -> None:
    candidate = Candidate(
        name="スパイスカレー作り",
        candidate_type="activity",
        domain="cooking",
        description="スパイスの配合を工夫する料理活動。",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    assert candidate.appeal_tags == []
    assert candidate.is_active is True
    assert candidate.genre is None
    assert candidate.created_at is not None
