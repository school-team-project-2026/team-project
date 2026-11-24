from typing import Literal

from pydantic import BaseModel, ConfigDict


class NegativePreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target: str
    strength: Literal["low_interest", "avoid"]
    evidence: str


class PreferenceFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    attributes: list[str]
    appeal_points: list[str]
    desired_experiences: list[str]
    values: list[str]
    keywords: list[str]

    negative_preferences: list[NegativePreference]
