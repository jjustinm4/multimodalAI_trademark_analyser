from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://trademark:trademark_dev@localhost:5432/trademark"
    llm_base_url: str = "http://localhost:8080/v1"
    llm_model: str = "gpt-oss-20b"
    llm_timeout_s: float = 110.0

    fusion_w_phonetic: float = 0.30
    fusion_w_semantic: float = 0.30
    fusion_w_visual: float = 0.20
    fusion_w_goods: float = 0.20

    embedding_device: str = "cuda"
    text_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    clip_model: str = "openai/clip-vit-base-patch32"


settings = Settings()
