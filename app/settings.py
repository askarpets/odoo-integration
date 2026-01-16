from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = ""

    ODOO_URL: str = ""
    ODOO_DATABASE: str = ""
    ODOO_USER: str = ""
    ODOO_PASSWORD: str = ""
    ODOO_FETCH_LIMIT: int = 100

    SYNC_INTERVAL_MINUTES: int = 30


settings = Settings()
