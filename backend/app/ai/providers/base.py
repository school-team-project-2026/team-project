from typing import Protocol

from app.ai.schemas import PreferenceFeatures


class PreferenceProvider(Protocol):
    provider_name: str
    model_name: str

    def extract(
        self,
        *,
        name: str,
        category: str,
        comment: str,
    ) -> PreferenceFeatures: ...
