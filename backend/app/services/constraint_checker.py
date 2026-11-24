from dataclasses import dataclass
from typing import Literal

from app.ai.schemas import NegativePreference
from app.models.candidate import Candidate

ConstraintStatus = Literal[
    "matched",
    "partially_matched",
    "not_matched",
    "unresolved",
]


# 現段階で明確に対応できる表現だけを登録する
TARGET_TO_MODE = {
    "自分で演奏すること": "perform",
    "演奏すること": "perform",
    "楽器を演奏すること": "perform",
    "自分で楽器を演奏すること": "perform",
    "バンドで演奏すること": "perform",
    "演奏する活動": "perform",
    "自分で楽器を弾くこと": "perform",
    "楽器を弾くこと": "perform",
    "自分で音楽を演奏すること": "perform",
    "楽器を自分で演奏すること": "perform",
}


@dataclass(frozen=True)
class ConstraintCheckResult:
    status: ConstraintStatus
    target: str
    strength: Literal["low_interest", "avoid"]
    matched_mode: str | None


def check_negative_preference(
    preference: NegativePreference,
    candidate: Candidate,
) -> ConstraintCheckResult:
    # 日本語の表記ゆれを一部吸収する
    normalized_target = "".join(preference.target.split())

    matched_mode = TARGET_TO_MODE.get(normalized_target)
    candidate_modes = candidate.interaction_modes

    if matched_mode is None or not candidate_modes:
        status: ConstraintStatus = "unresolved"

    elif matched_mode not in candidate_modes:
        status = "not_matched"

    elif len(set(candidate_modes)) > 1:
        status = "partially_matched"

    else:
        status = "matched"

    return ConstraintCheckResult(
        status=status,
        target=preference.target,
        strength=preference.strength,
        matched_mode=matched_mode,
    )
