from app.ai.providers.base import PreferenceProvider
from app.ai.schemas import PreferenceFeatures


class PreferenceExtractor:
    def __init__(self, provider: PreferenceProvider) -> None:
        self._provider = provider

    def extract(
        self,
        *,
        name: str,
        category: str,
        comment: str,
    ) -> PreferenceFeatures:
        return self._provider.extract(
            name=name,
            category=category,
            comment=comment,
        )
