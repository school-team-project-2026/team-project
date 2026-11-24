import pytest

from app.ai.schemas import NegativePreference
from app.models.candidate import Candidate
from app.services.constraint_checker import (
    check_negative_preference,
)


def make_candidate(
    modes: list[str] | None,
) -> Candidate:
    return Candidate(
        name="テスト候補",
        candidate_type="activity",
        domain="music",
        genre=None,
        description="テスト用のCandidate",
        appeal_tags=[],
        interaction_modes=modes,
    )


def make_preference(
    target: str,
    strength: str = "low_interest",
) -> NegativePreference:
    return NegativePreference(
        target=target,
        strength=strength,
        evidence="ユーザーの入力に基づくテスト",
    )


def test_perform_mode_is_matched() -> None:
    preference = make_preference("自分で演奏すること")
    candidate = make_candidate(["perform"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "matched"
    assert result.matched_mode == "perform"
    assert result.strength == "low_interest"


def test_listen_mode_is_not_matched() -> None:
    preference = make_preference("自分で演奏すること")
    candidate = make_candidate(["listen"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "not_matched"


def test_multiple_modes_are_partially_matched() -> None:
    preference = make_preference("自分で演奏すること")
    candidate = make_candidate(["listen", "perform"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "partially_matched"


def test_avoid_strength_is_preserved() -> None:
    preference = make_preference(
        "楽器を演奏すること",
        strength="avoid",
    )
    candidate = make_candidate(["perform"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "matched"
    assert result.strength == "avoid"


def test_unknown_target_is_unresolved() -> None:
    preference = make_preference(
        "高い場所",
        strength="avoid",
    )
    candidate = make_candidate(["participate"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "unresolved"
    assert result.matched_mode is None


def test_unclassified_candidate_is_unresolved() -> None:
    preference = make_preference("自分で演奏すること")
    candidate = make_candidate(None)

    result = check_negative_preference(preference, candidate)

    assert result.status == "unresolved"


def test_ambiguous_target_is_not_guessed() -> None:
    preference = make_preference("演奏")
    candidate = make_candidate(["perform"])

    result = check_negative_preference(preference, candidate)

    assert result.status == "unresolved"


@pytest.mark.parametrize(
    "target",
    [
        "自分で演奏すること",
        "自分で楽器を弾くこと",
        "楽器を弾くこと",
        "自分で音楽を演奏すること",
        "楽器を自分で演奏すること",
        "自分で 楽器を 演奏すること",
    ],
)
def test_perform_target_variations(target: str) -> None:
    preference = make_preference(target, strength="avoid")

    perform_candidate = make_candidate(["perform"])
    listen_candidate = make_candidate(["listen"])

    perform_result = check_negative_preference(
        preference,
        perform_candidate,
    )
    listen_result = check_negative_preference(
        preference,
        listen_candidate,
    )

    assert perform_result.status == "matched"
    assert perform_result.matched_mode == "perform"
    assert perform_result.strength == "avoid"

    assert listen_result.status == "not_matched"
