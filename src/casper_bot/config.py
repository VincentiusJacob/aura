from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    DATABASE_URL: str = ""
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def require(self, *fields: str) -> None:
        missing = [field for field in fields if not getattr(self, field, "")]
        if missing:
            missing_fields = ", ".join(missing)
            raise RuntimeError(
                f"Missing required environment variables: {missing_fields}. "
                "Set them in your shell or .env before starting the bot."
            )


settings = Settings()
