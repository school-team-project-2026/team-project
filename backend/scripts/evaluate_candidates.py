from collections import Counter

from sqlalchemy import select

from app.ai.embeddings.e5 import E5EmbeddingProvider
from app.ai.embeddings.text import candidate_to_text
from app.ai.similarity import cosine_similarity
from app.db.session import SessionLocal
from app.models.candidate import Candidate

EVALUATION_QUERIES = [
    (
        "RPG・戦略",
        "敵の弱点を突くターン制RPGの戦略を考えるのが好き",
    ),
    (
        "協力・作戦",
        "仲間と協力して作戦を立てるのが好き",
    ),
    (
        "料理・工夫",
        "スパイスの配合を変えて料理を工夫するのが好き",
    ),
    (
        "ジャズ",
        "ジャズの即興演奏や楽器の音色を楽しみたい",
    ),
    (
        "推理",
        "証言の矛盾や小さな手がかりから事件の真相を推理したい",
    ),
    (
        "宇宙・科学",
        "宇宙や相対性理論などの科学的なテーマを楽しみたい",
    ),
    (
        "空間パズル",
        "空間の構造や物体の配置を利用して謎を解くのが好き",
    ),
    (
        "音楽制作",
        "音色やメロディを組み合わせて自分で曲を作りたい",
    ),
    (
        "農場・生活",
        "農場を少しずつ発展させて自由な生活を楽しみたい",
    ),
    (
        "候補不足・陶芸",
        "ろくろで粘土を成形して陶器を作ることに興味がある",
    ),
]


def main() -> None:
    provider = E5EmbeddingProvider()

    with SessionLocal() as session:
        candidates = session.scalars(
            select(Candidate)
            .where(Candidate.is_active.is_(True))
            .order_by(Candidate.id)
        ).all()

        if not candidates:
            raise SystemExit("有効なCandidateがありません")

        # Candidate側は一度だけEmbeddingする
        candidate_vectors = [
            (
                candidate,
                provider.embed_passage(candidate_to_text(candidate)),
            )
            for candidate in candidates
        ]

        print(f"Candidate数: {len(candidate_vectors)}")
        print(f"評価入力数: {len(EVALUATION_QUERIES)}")

        top1_counts = Counter()
        top3_counts = Counter()

        for number, (label, query) in enumerate(
            EVALUATION_QUERIES,
            start=1,
        ):
            query_vector = provider.embed_query(query)

            scores = [
                (
                    candidate,
                    cosine_similarity(
                        query_vector,
                        candidate_vector,
                    ),
                )
                for candidate, candidate_vector in candidate_vectors
            ]

            scores.sort(key=lambda item: (-item[1], item[0].id))

            print(f"\n{'=' * 55}")
            print(f"TEST {number}: {label}")
            print(f"入力: {query}")
            print("-" * 55)

            for rank, (candidate, score) in enumerate(
                scores[:5],
                start=1,
            ):
                print(f"{rank}位: {candidate.name} [{candidate.domain}] / {score:.4f}")

            top1_counts[scores[0][0].name] += 1

            for candidate, _ in scores[:3]:
                top3_counts[candidate.name] += 1

            gap = scores[0][1] - scores[1][1]
            print(f"1位と2位の差: {gap:.4f}")

        print(f"\n{'=' * 55}")
        print("出現頻度まとめ")
        print("=" * 55)

        print("\n1位になった回数:")
        for name, count in top1_counts.most_common():
            print(f"  {name}: {count}回")

        print("\nTOP3登場回数:")
        for name, count in top3_counts.most_common():
            print(f"  {name}: {count}回")


if __name__ == "__main__":
    main()
