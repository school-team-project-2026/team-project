EXTRACTION_INSTRUCTIONS = """
You extract a user's preference features for a cross-domain recommendation system.

Rules:
- Treat the user's comment as the strongest evidence.
- Use the item name and category only as context.
- Do not invent preferences that the user did not express or strongly imply.
- Prefer concepts that can be compared across different domains such as
  media, sports, vehicles, music, travel, and other hobbies.
- If there is not enough evidence for a field, return an empty list.
- Keep each feature concise.
- Return features in Japanese.
""".strip()


def build_preference_prompt(
    *,
    name: str,
    category: str,
    comment: str,
) -> str:
    return f"""
{EXTRACTION_INSTRUCTIONS}

Interest Item:
name: {name}
category: {category}
comment: {comment}

Extract preference features from this Interest Item.
""".strip()
