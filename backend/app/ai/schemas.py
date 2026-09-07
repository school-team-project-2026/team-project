from pydantic import BaseModel, Field


class PreferenceFeatures(BaseModel):
    attributes: list[str] = Field(default_factory=list)
    appeal_points: list[str] = Field(default_factory=list)
    desired_experiences: list[str] = Field(default_factory=list)
    values: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
