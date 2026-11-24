from app.ai.embeddings.e5 import E5EmbeddingProvider
from app.ai.preference_extractor import PreferenceExtractor
from app.ai.providers.groq import GroqProvider
from app.db.session import SessionLocal
from app.schemas.recommendation import RecommendationRequest
from app.services.candidate_similarity import find_similar_candidates
from app.services.preference_aware_retrieval import (
    retrieve_preference_aware_candidates,
)


def main() -> None:
    request = RecommendationRequest(
        interest_text="ジャズ",
        liked_aspects=(
            "テンポの速い演奏や楽器同士の掛け合いを"
            "聴くのが好きです。自分で演奏することには"
            "特に興味はありません。"
        ),
    )

    embedding = E5EmbeddingProvider()
    extractor = PreferenceExtractor(GroqProvider())

    # 比較条件をそろえるため、Rawにも好きな理由を含める
    raw_query = f"興味: {request.interest_text}\n好きな理由: {request.liked_aspects}"

    with SessionLocal() as session:
        raw_results = find_similar_candidates(
            session=session,
            embedding_provider=embedding,
            query_text=raw_query,
            limit=5,
        )

        extracted_result = retrieve_preference_aware_candidates(
            session=session,
            request=request,
            extractor=extractor,
            embedding_provider_factory=lambda: embedding,
            limit=5,
        )

        print("\n========== 入力 ==========")
        print(raw_query)

        print("\n========== Raw検索 ==========")

        for rank, item in enumerate(raw_results, start=1):
            print(
                f"{rank}位: {item.candidate.name} "
                f"[{item.candidate.domain}] "
                f"/ {item.similarity:.4f}"
            )

        print("\n========== Extracted検索 ==========")
        print("検索方式:", extracted_result.search_method)

        if extracted_result.features is not None:
            print("\nGroqが抽出した特徴:")

            for key, values in extracted_result.features.model_dump().items():
                print(f"  {key}: {values}")

        print("\n実際の検索テキスト:")
        print(extracted_result.query_text)

        print("\n検索結果:")

        for rank, item in enumerate(
            extracted_result.candidates,
            start=1,
        ):
            print(
                f"{rank}位: {item.candidate.name} "
                f"[{item.candidate.domain}] "
                f"/ {item.similarity:.4f}"
            )


if __name__ == "__main__":
    main()
