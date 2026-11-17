from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.embeddings.base import EmbeddingProvider
from app.ai.embeddings.text import candidate_to_text
from app.ai.similarity import cosine_similarity
from app.models.candidate import Candidate


@dataclass(frozen=True)
class ScoredCandidate:
    candidate: Candidate
    similarity: float


def find_similar_candidates(
    session: Session,
    embedding_provider: EmbeddingProvider,
    query_text: str,
    limit: int = 5,
) -> list[ScoredCandidate]:
    if not query_text.strip():
        raise ValueError("Query text must not be empty")

    if limit <= 0:
        raise ValueError("Limit must be positive")

    candidates = session.scalars(
        select(Candidate).where(Candidate.is_active.is_(True)).order_by(Candidate.id)
    ).all()

    if not candidates:
        return []

    query_vector = embedding_provider.embed_query(query_text)

    scored_candidates = []

    for candidate in candidates:
        passage_text = candidate_to_text(candidate)
        passage_vector = embedding_provider.embed_passage(passage_text)

        similarity = cosine_similarity(
            query_vector,
            passage_vector,
        )

        scored_candidates.append(
            ScoredCandidate(
                candidate=candidate,
                similarity=similarity,
            )
        )

    scored_candidates.sort(
        key=lambda item: (
            -item.similarity,
            item.candidate.id,
        )
    )

    return scored_candidates[:limit]
