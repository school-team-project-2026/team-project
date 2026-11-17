from app.ai.embeddings.text import candidate_to_text
from app.models.candidate import Candidate


def test_candidate_to_text_with_genre_and_tags() -> None:
    candidate = Candidate(
        name="オクトパストラベラーII",
        candidate_type="work",
        domain="game",
        genre="turn_based_rpg",
        description="戦略性を特徴とするRPG。",
        appeal_tags=["戦略性", "弱点分析"],
    )

    result = candidate_to_text(candidate)

    assert "名称: オクトパストラベラーII" in result
    assert "分野: game" in result
    assert "ジャンル: turn_based_rpg" in result
    assert "説明: 戦略性を特徴とするRPG。" in result
    assert "魅力: 戦略性, 弱点分析" in result


def test_candidate_to_text_without_optional_fields() -> None:
    candidate = Candidate(
        name="ボルダリング",
        candidate_type="activity",
        domain="sports",
        genre=None,
        description="課題の完登を目指すスポーツ。",
        appeal_tags=[],
    )

    result = candidate_to_text(candidate)

    assert "名称: ボルダリング" in result
    assert "説明: 課題の完登を目指すスポーツ。" in result
    assert "ジャンル:" not in result
    assert "魅力:" not in result
