import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    MOCK_MODE: bool = os.getenv("MOCK_MODE", "true").lower() in ("1", "true", "yes")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    MAX_CONCURRENT_CALLS: int = int(os.getenv("MAX_CONCURRENT_CALLS", "1"))
    AI_TOKEN_LIMIT: int = int(os.getenv("AI_TOKEN_LIMIT", "2048"))
    MAX_GEMINI_RESPONSE_TOKENS: int = int(os.getenv("MAX_GEMINI_RESPONSE_TOKENS", "512"))
    MESSAGE_DELAY_MS: int = int(os.getenv("MESSAGE_DELAY_MS", "100"))
    RESPONSE_DELAY_MS: int = int(os.getenv("RESPONSE_DELAY_MS", "250"))
    DB_PROVIDER: str = os.getenv("DB_PROVIDER", "sqlite")
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", "/data/dev.db")
    STORE_RAW_AUDIO: bool = os.getenv("STORE_RAW_AUDIO", "false").lower() in ("1", "true", "yes")
    RECORDINGS_PATH: str = os.getenv("RECORDINGS_PATH", "/data/recordings")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9000"))
    AI_PROVIDER_API_KEY: str = os.getenv("AI_PROVIDER_API_KEY", "")


settings = Settings()
