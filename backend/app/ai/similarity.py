from collections.abc import Sequence
from math import sqrt


def cosine_similarity(
    left: Sequence[float],
    right: Sequence[float],
) -> float:
    if len(left) != len(right):
        raise ValueError("Vector dimensions must match")

    if not left:
        raise ValueError("Vectors must not be empty")

    dot_product = sum(a * b for a, b in zip(left, right))

    left_norm = sqrt(sum(value**2 for value in left))
    right_norm = sqrt(sum(value**2 for value in right))

    if left_norm == 0 or right_norm == 0:
        raise ValueError("Vectors must not be zero vectors")

    return dot_product / (left_norm * right_norm)
