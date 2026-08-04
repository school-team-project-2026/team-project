"""第1回バックエンド勉強会：講義中の小演習。"""


def exercise_1() -> None:
    """1から5まで表示する。"""
    # TODO: rangeを使って、1から5まで表示してください。
    pass


def exercise_2() -> None:
    """1から10までの奇数だけを表示する。"""
    # TODO: 1から10まで繰り返し、奇数だけ表示してください。
    pass


def exercise_3(scores: list[int]) -> list[int]:
    """80点以上の点数だけを返す。"""
    # TODO: 条件に合う点数を新しいlistへ追加して返してください。
    return []


def exercise_4(scores: list[int]) -> dict[str, int]:
    """件数・合計・最高点をdictにまとめる。"""
    # TODO: count / total / highest を返してください。
    return {}


def exercise_5(scores: list[int], threshold: int) -> list[int]:
    """基準点以上の点数だけを返す。"""
    # TODO: exercise_3を発展させてください。
    return []


def main() -> None:
    sample_scores = [80, 65, 90, 75, 100]
    print("演習1")
    exercise_1()
    print("\n演習2")
    exercise_2()
    print("\n演習3", exercise_3(sample_scores))
    print("演習4", exercise_4(sample_scores))
    print("演習5", exercise_5(sample_scores, 80))


if __name__ == "__main__":
    main()
