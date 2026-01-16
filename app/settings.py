from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # SQL DB
    DATABASE_URL: str = ""

    # Odoo API
    ODOO_URL: str = ""
    ODOO_DATABASE: str = ""
    ODOO_USER: str = ""
    ODOO_PASSWORD: str = ""
    ODOO_FETCH_LIMIT: int = 100

    # Data sync
    SYNC_INTERVAL_MINUTES: int = 30

    # JWT auth
    ACCESS_TOKEN_VERIFICATION_KEY: str = ""
    ACCESS_TOKEN_SIGNATURE_ALGORITHM: str = ""


settings = Settings()
