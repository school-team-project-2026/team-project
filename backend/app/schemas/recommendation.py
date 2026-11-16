from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints, field_validator


# Frontend → Backend
class RecommendationRequest(BaseModel):
    interest_text: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=200,
        ),
    ]

    liked_aspects: str | None = Field(
        default=None,
        max_length=1000,
    )

    @field_validator("liked_aspects")
    @classmethod
    def normalize_liked_aspects(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip() or None


# Backend → Frontend
class RecommendationAnalysis(BaseModel):
    summary: str
    features: list[str]
    basis: Literal["user_comment", "general_characteristics"]


class RecommendationItem(BaseModel):
    candidate_id: int
    name: str
    domain: str
    recommendation_type: Literal[
        "same_genre",
        "cross_genre",
        "adventure",
    ]
    reason: str


class RecommendationResponse(BaseModel):
    analysis: RecommendationAnalysis
    recommendations: list[RecommendationItem]
