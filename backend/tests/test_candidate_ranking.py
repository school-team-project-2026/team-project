from app.ai.schemas import NegativePreference
from app.models.candidate import Candidate
from app.services.candidate_ranking import rank_candidates
from app.services.candidate_similarity import ScoredCandidate


def make_scored_candidate(
    candidate_id: int,
    name: str,
    modes: list[str] | None,
    similarity: float,
) -> ScoredCandidate:
    candidate = Candidate(
        id=candidate_id,
        name=name,
        candidate_type="activity",
        domain="music",
        genre=None,
        description="テスト用",
        appeal_tags=[],
        interaction_modes=modes,
    )
    return ScoredCandidate(
        candidate=candidate,
        similarity=similarity,
    )


def make_preference(
    target: str,
    strength: str,
) -> NegativePreference:
    return NegativePreference(
        target=target,
        strength=strength,
        evidence="テスト用の発言",
    )


def test_candidates_are_sorted_by_similarity() -> None:
    candidates = [
        make_scored_candidate(1, "A", ["listen"], 0.7),
        make_scored_candidate(2, "B", ["listen"], 0.9),
    ]

    result = rank_candidates(candidates, [])

    names = [entry.scored_candidate.candidate.name for entry in result.eligible]

    assert names == ["B", "A"]


def test_low_interest_deprioritizes_performing() -> None:
    candidates = [
        make_scored_candidate(1, "ジャズ鑑賞", ["listen"], 0.80),
        make_scored_candidate(2, "バンドでの合奏", ["perform"], 0.95),
    ]

    preferences = [
        make_preference(
            "自分で演奏すること",
            "low_interest",
        )
    ]

    result = rank_candidates(candidates, preferences)

    assert len(result.eligible) == 1
    assert len(result.deprioritized) == 1
    assert result.eligible[0].scored_candidate.candidate.name == ("ジャズ鑑賞")
    assert result.deprioritized[0].scored_candidate.candidate.name == ("バンドでの合奏")


def test_avoid_excludes_confirmed_match() -> None:
    candidates = [
        make_scored_candidate(1, "バンドでの合奏", ["perform"], 0.95),
    ]

    preferences = [
        make_preference(
            "自分で演奏すること",
            "avoid",
        )
    ]

    result = rank_candidates(candidates, preferences)

    assert result.eligible == []
    assert len(result.excluded) == 1


def test_partial_avoid_is_held() -> None:
    candidates = [
        make_scored_candidate(
            1,
            "複合音楽活動",
            ["listen", "perform"],
            0.90,
        )
    ]

    preferences = [
        make_preference(
            "自分で演奏すること",
            "avoid",
        )
    ]

    result = rank_candidates(candidates, preferences)

    assert len(result.held) == 1
    assert result.excluded == []


def test_unknown_avoid_is_held() -> None:
    candidates = [make_scored_candidate(1, "ボルダリング", ["participate"], 0.9)]

    preferences = [make_preference("高い場所", "avoid")]

    result = rank_candidates(candidates, preferences)

    assert result.eligible == []
    assert len(result.held) == 1
    assert result.held[0].checks[0].status == "unresolved"


def test_avoid_takes_priority_over_low_interest() -> None:
    candidates = [make_scored_candidate(1, "バンドでの合奏", ["perform"], 0.95)]

    preferences = [
        make_preference("自分で演奏すること", "low_interest"),
        make_preference("楽器を弾くこと", "avoid"),
    ]

    result = rank_candidates(candidates, preferences)

    assert len(result.excluded) == 1
    assert result.deprioritized == []
    assert result.eligible == []


def test_unknown_avoid_holds_all_candidates() -> None:
    candidates = [
        make_scored_candidate(1, "ジャズ鑑賞", ["listen"], 0.9),
        make_scored_candidate(2, "バンド活動", ["perform"], 0.8),
    ]

    preferences = [make_preference("高い場所", "avoid")]

    result = rank_candidates(candidates, preferences)

    assert len(result.held) == 2
    assert result.eligible == []
    assert result.deprioritized == []
    assert result.excluded == []


def test_equal_similarity_is_sorted_by_candidate_id() -> None:
    candidates = [
        make_scored_candidate(2, "B", ["listen"], 0.9),
        make_scored_candidate(1, "A", ["listen"], 0.9),
    ]

    result = rank_candidates(candidates, [])

    ids = [entry.scored_candidate.candidate.id for entry in result.eligible]

    assert ids == [1, 2]
