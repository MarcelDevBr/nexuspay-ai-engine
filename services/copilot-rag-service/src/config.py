from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    ENV: str = "development"
    POSTGRES_URL: str = "postgresql://nexus_user:nexus_password@localhost:5432/nexuspay_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AWS Bedrock Config
    AWS_REGION: str = "us-east-1"
    USE_MOCK_LLM: bool = True
    MAX_TOKENS_PER_REQUEST: int = 1000

settings = Settings()
