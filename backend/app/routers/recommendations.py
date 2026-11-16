from fastapi import APIRouter

from app.schemas.recommendation import (
    RecommendationAnalysis,
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=200,
)
def create_recommendations(
    request: RecommendationRequest,
) -> RecommendationResponse:
    """固定サンプルの推薦結果を返す開発用API。"""

    has_reason = request.liked_aspects is not None

    analysis = RecommendationAnalysis(
        summary=(
            "好きな理由を受け取りました。現在は固定サンプルによる表示テストです。"
            if has_reason
            else "好きな理由は未入力です。現在は固定サンプルによる表示テストです。"
        ),
        features=[
            "サンプル：戦略性",
            "サンプル：試行錯誤",
            "サンプル：達成感",
        ],
        basis=("user_comment" if has_reason else "general_characteristics"),
    )

    recommendations = [
        RecommendationItem(
            candidate_id=101,
            name="オクトパストラベラーII",
            domain="ゲーム",
            recommendation_type="same_genre",
            reason="【サンプル】敵の弱点を考える戦闘が特徴です。",
        ),
        RecommendationItem(
            candidate_id=102,
            name="パンデミック",
            domain="ボードゲーム",
            recommendation_type="cross_genre",
            reason="【サンプル】行動計画を立てる楽しさがあります。",
        ),
        RecommendationItem(
            candidate_id=103,
            name="ボルダリング",
            domain="スポーツ",
            recommendation_type="cross_genre",
            reason="【サンプル】攻略手順を考えて挑戦できます。",
        ),
        RecommendationItem(
            candidate_id=104,
            name="リアル脱出ゲーム",
            domain="謎解き",
            recommendation_type="cross_genre",
            reason="【サンプル】分析と試行錯誤が楽しめます。",
        ),
        RecommendationItem(
            candidate_id=105,
            name="スパイスカレー作り",
            domain="料理",
            recommendation_type="adventure",
            reason="【サンプル】組み合わせを工夫する体験です。",
        ),
    ]

    return RecommendationResponse(
        analysis=analysis,
        recommendations=recommendations,
    )
