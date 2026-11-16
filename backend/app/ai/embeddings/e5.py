from sentence_transformers import SentenceTransformer

from app.core.config import settings


class E5EmbeddingProvider:
    provider_name = "sentence-transformers"

    def __init__(self) -> None:
        self.model_name = settings.embedding_model
        self._model = SentenceTransformer(self.model_name)

        dimensions = self._model.get_embedding_dimension()

        if dimensions is None:
            raise RuntimeError("Could not determine embedding dimensions")

        self.dimensions = dimensions

    def embed_query(self, text: str) -> list[float]:
        return self._embed("query", text)

    def embed_passage(self, text: str) -> list[float]:
        return self._embed("passage", text)

    def _embed(self, prefix: str, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Embedding text must not be empty")

        vector = self._model.encode(
            f"{prefix}: {text}",
            normalize_embeddings=True,
        )

        return vector.tolist()
