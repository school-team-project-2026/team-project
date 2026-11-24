from dataclasses import dataclass
from typing import Literal

from app.ai.schemas import NegativePreference
from app.services.candidate_similarity import ScoredCandidate
from app.services.constraint_checker import (
    ConstraintCheckResult,
    check_negative_preference,
)

RankingDecision = Literal[
    "eligible",
    "deprioritized",
    "held",
    "excluded",
]


@dataclass(frozen=True)
class RankingEntry:
    scored_candidate: ScoredCandidate
    decision: RankingDecision
    checks: list[ConstraintCheckResult]


@dataclass(frozen=True)
class RankingResult:
    eligible: list[RankingEntry]
    deprioritized: list[RankingEntry]
    held: list[RankingEntry]
    excluded: list[RankingEntry]


def decide_candidate(
    checks: list[ConstraintCheckResult],
) -> RankingDecision:
    # 明確な拒否と完全一致した場合は除外
    if any(check.strength == "avoid" and check.status == "matched" for check in checks):
        return "excluded"

    # 強い拒否について判断が曖昧な候補は保留
    if any(
        check.strength == "avoid"
        and check.status in {"partially_matched", "unresolved"}
        for check in checks
    ):
        return "held"

    # 興味が薄い活動は順位を後回しにする
    if any(
        check.strength == "low_interest"
        and check.status in {"matched", "partially_matched"}
        for check in checks
    ):
        return "deprioritized"

    return "eligible"


def rank_candidates(
    scored_candidates: list[ScoredCandidate],
    negative_preferences: list[NegativePreference],
) -> RankingResult:
    groups: dict[RankingDecision, list[RankingEntry]] = {
        "eligible": [],
        "deprioritized": [],
        "held": [],
        "excluded": [],
    }

    for scored in scored_candidates:
        checks = [
            check_negative_preference(
                preference,
                scored.candidate,
            )
            for preference in negative_preferences
        ]

        decision = decide_candidate(checks)

        groups[decision].append(
            RankingEntry(
                scored_candidate=scored,
                decision=decision,
                checks=checks,
            )
        )

    # 各グループ内はSimilarityの高い順にする
    for entries in groups.values():
        entries.sort(
            key=lambda entry: (
                -entry.scored_candidate.similarity,
                entry.scored_candidate.candidate.id,
            )
        )

    return RankingResult(
        eligible=groups["eligible"],
        deprioritized=groups["deprioritized"],
        held=groups["held"],
        excluded=groups["excluded"],
    )
