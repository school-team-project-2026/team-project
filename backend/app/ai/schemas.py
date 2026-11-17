from pydantic import BaseModel, ConfigDict


class PreferenceFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    attributes: list[str]
    appeal_points: list[str]
    desired_experiences: list[str]
    values: list[str]
    keywords: list[str]
