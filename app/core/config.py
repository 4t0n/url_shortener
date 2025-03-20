from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.
    """

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    )

    TEST_DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/test_db"
    )
    ALLOWED_DOMAINS: list[str] = ["127.0.0.1"]
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "postgres"
    TEST_DATABASE_NAME: str = "test_db"
    TEST_DATABASE_USER: str = "postgres"
    TEST_DATABASE_PASSWORD: str = "postgres"
    TEST_DATABASE_HOST: str = "db_test"
    LOCAL_DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    )

    model_config = {
        "env_file": ".env",
    }


settings = Settings()  # type: ignore
