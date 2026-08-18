from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    ENV: str = "development"
    POSTGRES_URL: str = "postgresql://nexus_user:nexus_password@localhost:5432/nexuspay_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AWS Config
    AWS_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    SQS_QUEUE_URL: str = "http://localhost:4566/000000000000/transacoes-events"
    
    # FinOps & Mock Controls (Garante 100% gratuidade no portfólio)
    USE_MOCK_LLM: bool = True
    MAX_TOKENS_PER_REQUEST: int = 1000
    DAILY_BUDGET_DOLLARS: float = 0.0 # Trava de custo zero

settings = Settings()
