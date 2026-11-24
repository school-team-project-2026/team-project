import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from sqlalchemy.orm import Session

from app.ai.embeddings.base import EmbeddingProvider
from app.ai.embeddings.text import preference_features_to_text
from app.ai.preference_extractor import PreferenceExtractor
from app.ai.schemas import PreferenceFeatures
from app.schemas.recommendation import RecommendationRequest
from app.services.candidate_ranking import (
    RankingResult,
    rank_candidates,
)
from app.services.candidate_similarity import (
    ScoredCandidate,
    find_similar_candidates,
)

logger = logging.getLogger(__name__)


class PreferenceExtractionError(RuntimeError):
    """好きな理由の特徴抽出に失敗したことを表す。"""


class EmbeddingInitializationError(RuntimeError):
    """EmbeddingProviderの初期化に失敗したことを表す。"""


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
    extractor: PreferenceExtractor | None,
    embedding_provider_factory: Callable[[], EmbeddingProvider],
    limit: int | None = 5,
) -> PreferenceAwareResult:

    query_text = request.interest_text

    search_method: Literal["raw", "extracted"] = "raw"
    features: PreferenceFeatures | None = None

    if request.liked_aspects:
        if extractor is None:
            raise PreferenceExtractionError("好きな理由の解析にはExtractorが必要です。")

        try:
            extracted = extractor.extract(
                name=request.interest_text,
                category="未指定",
                comment=request.liked_aspects,
            )

            features = extracted

            extracted_text = preference_features_to_text(extracted).strip()

            if extracted_text:
                query_text = extracted_text
                search_method = "extracted"

        except Exception as exc:
            logger.warning(
                "Preference extraction failed; stopping retrieval (%s)",
                type(exc).__name__,
            )
            raise PreferenceExtractionError("Preference extraction failed") from exc

    try:
        embedding_provider = embedding_provider_factory()
    except Exception as exc:
        logger.warning(
            "Embedding initialization failed (%s)",
            type(exc).__name__,
        )
        raise EmbeddingInitializationError("Embedding initialization failed") from exc

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


@dataclass(frozen=True)
class RankedPreferenceAwareResult:
    retrieval: PreferenceAwareResult
    ranking: RankingResult


def retrieve_ranked_preference_aware_candidates(
    *,
    session: Session,
    request: RecommendationRequest,
    extractor: PreferenceExtractor | None,
    embedding_provider_factory: Callable[[], EmbeddingProvider],
) -> RankedPreferenceAwareResult:
    retrieval = retrieve_preference_aware_candidates(
        session=session,
        request=request,
        extractor=extractor,
        embedding_provider_factory=embedding_provider_factory,
        limit=None,
    )

    negative_preferences = (
        retrieval.features.negative_preferences
        if retrieval.features is not None
        else []
    )

    ranking = rank_candidates(
        retrieval.candidates,
        negative_preferences,
    )

    return RankedPreferenceAwareResult(
        retrieval=retrieval,
        ranking=ranking,
    )
