from google import genai

from app.ai.prompts import build_preference_prompt
from app.ai.schemas import PreferenceFeatures
from app.core.config import settings


class GeminiProvider:
    provider_name = "google"

    def __init__(self) -> None:
        if settings.gemini_api_key is None:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        self.model_name = settings.gemini_model
        self._client = genai.Client(api_key=settings.gemini_api_key.get_secret_value())

    def extract(
        self,
        *,
        name: str,
        category: str,
        comment: str,
    ) -> PreferenceFeatures:
        prompt = build_preference_prompt(
            name=name,
            category=category,
            comment=comment,
        )

        response = self._client.interactions.create(
            model=self.model_name,
            input=prompt,
            generation_config={
                "thinking_level": "low",
            },
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": PreferenceFeatures.model_json_schema(),
            },
        )

        return PreferenceFeatures.model_validate_json(response.output_text)
