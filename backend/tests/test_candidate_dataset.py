from collections import Counter

from scripts.seed_candidates import SEED_CANDIDATES


def test_dataset_size_and_domain_balance() -> None:
    counts = Counter(item["domain"] for item in SEED_CANDIDATES)

    assert len(SEED_CANDIDATES) == 24
    assert len(counts) == 8
    assert all(count == 3 for count in counts.values())


def test_candidate_names_are_unique_within_domain() -> None:
    keys = [
        (item["name"].strip().casefold(), item["domain"]) for item in SEED_CANDIDATES
    ]

    assert len(keys) == len(set(keys))


def test_candidate_required_fields() -> None:
    allowed_types = {"work", "activity", "experience"}

    for item in SEED_CANDIDATES:
        assert item["name"].strip()
        assert item["candidate_type"] in allowed_types
        assert item["domain"].strip()
        assert item["description"].strip()
        assert 3 <= len(item["appeal_tags"]) <= 5
        assert len(item["appeal_tags"]) == len(set(item["appeal_tags"]))
