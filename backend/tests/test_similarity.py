import pytest

from app.ai.similarity import cosine_similarity


def test_identical_vectors() -> None:
    result = cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    )
    assert result == pytest.approx(1.0)


def test_orthogonal_vectors() -> None:
    result = cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )
    assert result == pytest.approx(0.0)


def test_opposite_vectors() -> None:
    result = cosine_similarity(
        [1.0, 0.0],
        [-1.0, 0.0],
    )
    assert result == pytest.approx(-1.0)


def test_different_dimensions() -> None:
    with pytest.raises(ValueError):
        cosine_similarity(
            [1.0, 0.0],
            [1.0, 0.0, 0.0],
        )


def test_zero_vector() -> None:
    with pytest.raises(ValueError):
        cosine_similarity(
            [0.0, 0.0],
            [1.0, 0.0],
        )
