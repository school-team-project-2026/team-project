from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Candidate

SEED_CANDIDATES = [
    {
        "name": "オクトパストラベラーII",
        "candidate_type": "work",
        "domain": "game",
        "genre": "turn_based_rpg",
        "description": (
            "敵の弱点を突くブレイクシステムやBP管理を特徴とするターン制RPG。"
        ),
        "appeal_tags": [
            "戦略性",
            "弱点分析",
            "リソース管理",
        ],
    },
    {
        "name": "パンデミック",
        "candidate_type": "work",
        "domain": "board_game",
        "genre": "cooperative",
        "description": ("プレイヤー同士で協力し、感染症の拡大を防ぐボードゲーム。"),
        "appeal_tags": [
            "協力",
            "行動計画",
            "リソース管理",
        ],
    },
    {
        "name": "ボルダリング",
        "candidate_type": "activity",
        "domain": "sports",
        "genre": None,
        "description": (
            "手足の運び方を考えながら、設定された課題の完登を目指すスポーツ。"
        ),
        "appeal_tags": [
            "試行錯誤",
            "課題攻略",
            "達成感",
        ],
    },
    {
        "name": "リアル脱出ゲーム",
        "candidate_type": "experience",
        "domain": "puzzle",
        "genre": "escape_room",
        "description": (
            "手がかりを集め、謎を解きながら目標達成を目指す体験型イベント。"
        ),
        "appeal_tags": [
            "謎解き",
            "分析",
            "問題解決",
        ],
    },
    {
        "name": "スパイスカレー作り",
        "candidate_type": "activity",
        "domain": "cooking",
        "genre": None,
        "description": ("スパイスの種類や配合を工夫し、好みの味を追求する料理活動。"),
        "appeal_tags": [
            "組み合わせ",
            "試行錯誤",
            "創造性",
        ],
    },
]


def seed_candidates() -> None:
    added = 0
    skipped = 0

    with SessionLocal() as session:
        for data in SEED_CANDIDATES:
            existing_id = session.scalar(
                select(Candidate.id).where(
                    Candidate.name == data["name"],
                    Candidate.domain == data["domain"],
                )
            )

            if existing_id is not None:
                skipped += 1
                continue

            session.add(Candidate(**data))
            added += 1

        session.commit()

    print(f"追加: {added}件 / 登録済み: {skipped}件")


if __name__ == "__main__":
    seed_candidates()
