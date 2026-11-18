import logging
from dataclasses import dataclass
from typing import Literal

from sqlalchemy.orm import Session

from app.ai.embeddings.base import EmbeddingProvider
from app.ai.embeddings.text import preference_features_to_text
from app.ai.preference_extractor import PreferenceExtractor
from app.ai.schemas import PreferenceFeatures
from app.schemas.recommendation import RecommendationRequest
from app.services.candidate_similarity import (
    ScoredCandidate,
    find_similar_candidates,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PreferenceAwareResult:
    query_text: str
    search_method: Literal["raw", "extracted"]
    features: PreferenceFeatures | None
    candidates: list[ScoredCandidate]


def retrieve_preference_aware_candidates(
    *,
    session: Session,
    request: RecommendationRequest,
    extractor: PreferenceExtractor,
    embedding_provider: EmbeddingProvider,
    limit: int = 5,
) -> PreferenceAwareResult:

    raw_query = request.interest_text

    if request.liked_aspects:
        raw_query = (
            f"興味: {request.interest_text}\n好きな理由: {request.liked_aspects}"
        )

    query_text = raw_query

    search_method: Literal["raw", "extracted"] = "raw"
    features: PreferenceFeatures | None = None

    if request.liked_aspects:
        try:
            extracted = extractor.extract(
                name=request.interest_text,
                category="未指定",
                comment=request.liked_aspects,
            )

            extracted_text = preference_features_to_text(extracted).strip()

            if extracted_text:
                query_text = extracted_text
                search_method = "extracted"
                features = extracted

        except Exception as exc:
            logger.warning(
                "Preference extraction failed; falling back to raw query (%s)",
                type(exc).__name__,
            )

    candidates = find_similar_candidates(
        session=session,
        embedding_provider=embedding_provider,
        query_text=query_text,
        limit=limit,
    )

    return PreferenceAwareResult(
        query_text=query_text,
        search_method=search_method,
        features=features,
        candidates=candidates,
    )
