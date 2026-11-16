from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int = 5432

    gemini_api_key: SecretStr | None = None
    gemini_model: str = "gemini-3.8-flash"

    groq_api_key: SecretStr | None = None
    groq_model: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )

    embedding_model: str = "intfloat/multilingual-e5-small"


settings = Settings()
