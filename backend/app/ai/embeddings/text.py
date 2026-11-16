from app.ai.schemas import PreferenceFeatures


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
