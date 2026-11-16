from typing import Protocol


class EmbeddingProvider(Protocol):
    provider_name: str
    model_name: str
    dimensions: int

    def embed_query(self, text: str) -> list[float]: ...

    def embed_passage(self, text: str) -> list[float]: ...
