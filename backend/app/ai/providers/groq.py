from groq import Groq

from app.ai.prompts import build_preference_prompt
from app.ai.schemas import PreferenceFeatures
from app.core.config import settings


class GroqProvider:
    provider_name = "groq"

    def __init__(self) -> None:
        if settings.groq_api_key is None:
            raise RuntimeError("GROQ_API_KEY is not configured")

        self.model_name = settings.groq_model
        self._client = Groq(api_key=settings.groq_api_key.get_secret_value())

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

        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            reasoning_effort="low",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "preference_features",
                    "strict": True,
                    "schema": PreferenceFeatures.model_json_schema(),
                },
            },
        )

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError("Groq returned no response content")

        return PreferenceFeatures.model_validate_json(content)
