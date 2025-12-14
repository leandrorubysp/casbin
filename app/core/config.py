from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "FastAPI Casbin Example"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "appdb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/appdb"
    )

    CASBIN_MODEL_PATH: str = "casbin_model.conf"
    CASBIN_TABLE_NAME: str = "casbin_rule"


settings = Settings()