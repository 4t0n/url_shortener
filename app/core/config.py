from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.
    """
    DATABASE_URL: str
    TEST_DATABASE: str
    ALLOWED_DOMAINS: list[str]

    model_config = {
        "env_file": ".env",
    }


settings = Settings()  # type: ignore
