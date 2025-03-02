from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALLOWED_DOMAINS: list[str]

    model_config = {
        "env_file": ".env",
    }


settings = Settings()  # type: ignore
