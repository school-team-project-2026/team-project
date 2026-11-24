import pytest
from pydantic import ValidationError

from app.ai.embeddings.text import preference_features_to_text
from app.ai.schemas import NegativePreference, PreferenceFeatures


def make_features(
    negative_preferences: list[NegativePreference],
) -> PreferenceFeatures:
    return PreferenceFeatures(
        attributes=["速いテンポ"],
        appeal_points=["楽器の掛け合い"],
        desired_experiences=["音楽を聴く"],
        values=[],
        keywords=["ジャズ"],
        negative_preferences=negative_preferences,
    )


def test_low_interest_preference() -> None:
    preference = NegativePreference(
        target="自分で演奏すること",
        strength="low_interest",
        evidence="自分で演奏することには特に興味はありません",
    )

    features = make_features([preference])

    assert features.negative_preferences[0].strength == "low_interest"
    assert features.negative_preferences[0].target == ("自分で演奏すること")
    assert "興味はありません" in (features.negative_preferences[0].evidence)


def test_avoid_preference() -> None:
    preference = NegativePreference(
        target="高い場所で行う活動",
        strength="avoid",
        evidence="高い場所で行う活動は絶対に避けたいです",
    )

    features = make_features([preference])

    assert features.negative_preferences[0].strength == "avoid"


def test_empty_negative_preferences_is_valid() -> None:
    features = make_features([])

    assert features.negative_preferences == []


def test_invalid_strength_is_rejected() -> None:
    with pytest.raises(ValidationError):
        NegativePreference(
            target="高い場所",
            strength="dislike",
            evidence="高い場所は苦手です",
        )


def test_negative_preferences_are_not_embedded_as_positive_features() -> None:
    features = make_features(
        [
            NegativePreference(
                target="自分で演奏すること",
                strength="low_interest",
                evidence="演奏には興味がありません",
            )
        ]
    )

    text = preference_features_to_text(features)

    assert "速いテンポ" in text
    assert "楽器の掛け合い" in text
    assert "自分で演奏すること" not in text
    assert "演奏には興味がありません" not in text
