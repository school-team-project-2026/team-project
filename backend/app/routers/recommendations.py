from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.embeddings.base import EmbeddingProvider
from app.ai.embeddings.e5 import E5EmbeddingProvider
from app.ai.preference_extractor import PreferenceExtractor
from app.ai.providers.groq import GroqProvider
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.schemas.recommendation import (
    RecommendationAnalysis,
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
    RecommendationUnavailableResponse,
)
from app.services.preference_aware_retrieval import (
    EmbeddingInitializationError,
    PreferenceExtractionError,
    retrieve_ranked_preference_aware_candidates,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)

DOMAIN_LABELS = {
    "game": "ゲーム",
    "board_game": "ボードゲーム",
    "sports": "スポーツ",
    "puzzle": "謎解き",
    "cooking": "料理",
    "music": "音楽",
    "book": "読書",
    "movie": "映画",
}

# MVP用の限定的な分野推定
DOMAIN_KEYWORDS = {
    "game": ("ゲーム", "rpg", "ドラクエ"),
    "board_game": ("ボードゲーム", "ボドゲ"),
    "sports": ("スポーツ", "バドミントン", "ボルダリング"),
    "puzzle": ("謎解き", "脱出ゲーム", "パズル", "数独"),
    "cooking": ("料理", "お菓子作り", "パン作り"),
    "music": ("ジャズ", "音楽", "クラシック"),
    "book": ("読書", "小説", "書籍"),
    "movie": ("映画", "シネマ"),
}


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


@lru_cache(maxsize=1)
def get_cached_extractor() -> PreferenceExtractor:
    return PreferenceExtractor(GroqProvider())


def get_extractor(
    request: RecommendationRequest,
) -> PreferenceExtractor | None:
    if not request.liked_aspects:
        return None

    try:
        return get_cached_extractor()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="好きな理由の解析サービスを利用できません。",
        ) from exc


@lru_cache(maxsize=1)
def get_embedding_provider() -> E5EmbeddingProvider:
    return E5EmbeddingProvider()


def get_embedding_provider_factory() -> Callable[[], EmbeddingProvider]:
    return get_embedding_provider


def infer_domain(interest_text: str) -> str | None:
    text = interest_text.casefold()

    matches = [
        domain
        for domain, keywords in DOMAIN_KEYWORDS.items()
        if any(keyword.casefold() in text for keyword in keywords)
    ]

    return matches[0] if len(matches) == 1 else None


def build_reason(candidate: Candidate) -> str:
    if candidate.appeal_tags:
        tags = "・".join(candidate.appeal_tags[:3])
        return f"この候補には、{tags}という特徴があります。"

    return candidate.description


@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=200,
    summary="趣味・作品の推薦",
    description=(
        "入力された趣味と好きな理由を基に推薦候補を検索します。"
        "明示された非希望を考慮し、0〜5件の候補を返します。"
    ),
    responses={
        503: {
            "model": RecommendationUnavailableResponse,
            "description": (
                "特徴抽出サービスの初期化・解析失敗、"
                "またはEmbeddingモデルの初期化失敗。"
                ),
        },
    },
)
def create_recommendations(
    request: RecommendationRequest,
    session: Annotated[Session, Depends(get_session)],
    extractor: Annotated[PreferenceExtractor | None, Depends(get_extractor)],
    embedding_provider_factory: Annotated[
        Callable[[], EmbeddingProvider],
        Depends(get_embedding_provider_factory),
    ],
) -> RecommendationResponse:
    # 好きな理由の解析に失敗した場合は、
    # 候補検索を続行せず503を返す。

    try:
        result = retrieve_ranked_preference_aware_candidates(
            session=session,
            request=request,
            extractor=extractor,
            embedding_provider_factory=embedding_provider_factory,
        )
    except PreferenceExtractionError as exc:
        raise HTTPException(
            status_code=503,
            detail=("好きな理由の解析に失敗しました。時間をおいて再度お試しください。"),
        ) from exc
    except EmbeddingInitializationError as exc:
        raise HTTPException(
            status_code=503,
            detail=("推薦モデルを利用できません。時間をおいて再度お試しください。"),
        ) from exc

    retrieval = result.retrieval
    ranking = result.ranking

    # 低関心は後回し。保留・除外は表示しない。
    display_entries = (ranking.eligible + ranking.deprioritized)[:5]

    source_domain = infer_domain(request.interest_text)

    recommendations = []

    for entry in display_entries:
        candidate = entry.scored_candidate.candidate

        # 暫定分類：同じDomainなら同系統。
        # Domain不明の場合は探索候補として扱う。
        recommendation_type = (
            "same_genre"
            if source_domain is not None and candidate.domain == source_domain
            else "cross_genre"
        )

        reason = build_reason(candidate)

        if entry.decision == "deprioritized":
            reason += " なお、入力された消極的な希望に関連するため、優先度は低めです。"

        recommendations.append(
            RecommendationItem(
                candidate_id=candidate.id,
                name=candidate.name,
                domain=DOMAIN_LABELS.get(
                    candidate.domain,
                    candidate.domain,
                ),
                recommendation_type=recommendation_type,
                reason=reason,
            )
        )

    features = []

    if retrieval.features is not None:
        extracted = retrieval.features
        raw_features = (
            extracted.appeal_points
            + extracted.desired_experiences
            + extracted.attributes
        )
        features = list(dict.fromkeys(raw_features))[:8]

    if not recommendations:
        summary = "現在の候補と制約条件では、推薦可能な趣味を確定できませんでした。"
    elif retrieval.search_method == "extracted":
        summary = (
            "好きな理由を分析し、趣味の特徴と"
            "明示された非希望を考慮して候補を選びました。"
        )
    else:
        summary = "入力内容を基に、趣味の特徴が近い候補を検索しました。"

    analysis = RecommendationAnalysis(
        summary=summary,
        features=features,
        basis=("user_comment" if request.liked_aspects else "general_characteristics"),
    )

    return RecommendationResponse(
        analysis=analysis,
        recommendations=recommendations,
    )
