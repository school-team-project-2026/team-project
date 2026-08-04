"""第1回バックエンド勉強会：宿題（10〜15分）。"""


def filter_high_scores(scores: list[int], threshold: int) -> list[int]:
    """基準点以上の点数だけを、元の順番で返す。"""
    # TODO: 処理を実装してください。
    return []


# Q1. この関数の入力は何ですか？
# 回答:
#
# Q2. この関数の出力は何ですか？
# 回答:
#
# Q3. thresholdが80の場合、80点は結果に含まれますか？
# 回答:
#
# Q4. scoresが空の場合、何が返りますか？
# 回答:


def main() -> None:
    scores = [80, 65, 90, 75, 100]
    print(filter_high_scores(scores, 80))
    print(filter_high_scores(scores, 90))
    print(filter_high_scores([], 80))


if __name__ == "__main__":
    main()
