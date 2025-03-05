from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.
    """
    DATABASE_URL: str = "sqlite+aiosqlite:///./my_db.db"
    TEST_DATABASE: str = "sqlite+aiosqlite:///:memory:"
    ALLOWED_DOMAINS: list[str] = ["127.0.0.1"]

    model_config = {
        "env_file": ".env",
    }


settings = Settings()  # type: ignore
