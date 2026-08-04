"""第1回バックエンド勉強会：統合課題。"""


def summarize_scores(scores: list[int]) -> dict[str, int | float]:
    """評価点一覧を集計する。"""
    # 入力:
    #
    # 処理:
    #
    # 出力:
    #
    # TODO: count / total / average / highest / lowest / high_score_count を返す。
    return {}


def main() -> None:
    sample_scores = [80, 65, 90, 75, 100]
    result = summarize_scores(sample_scores)
    expected = {
        "count": 5,
        "total": 410,
        "average": 82.0,
        "highest": 100,
        "lowest": 65,
        "high_score_count": 3,
    }
    print("結果:", result)
    print("期待値:", expected)
    print("一致:", result == expected)


if __name__ == "__main__":
    main()
