from app.ai.schemas import PreferenceFeatures
from app.models.candidate import Candidate


def preference_features_to_text(features: PreferenceFeatures) -> str:
    sections = [
        ("属性", features.attributes),
        ("魅力", features.appeal_points),
        ("求める体験", features.desired_experiences),
        ("価値観", features.values),
        ("キーワード", features.keywords),
    ]

    return "\n".join(
        f"{label}: {', '.join(values)}" for label, values in sections if values
    )


def candidate_to_text(candidate: Candidate) -> str:
    sections = [
        f"名称: {candidate.name}",
        f"分野: {candidate.domain}",
        f"種類: {candidate.candidate_type}",
    ]

    if candidate.genre:
        sections.append(f"ジャンル: {candidate.genre}")

    sections.append(f"説明: {candidate.description}")

    if candidate.appeal_tags:
        sections.append(f"魅力: {', '.join(candidate.appeal_tags)}")

    return "\n".join(sections)
