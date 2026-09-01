from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InterestItemBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=50)
    comment: str = Field(min_length=1)


class InterestItemCreate(InterestItemBase):
    pass


class InterestItemRead(InterestItemBase):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True,
    )

    id: int
    created_at: datetime
