from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    ENV: str = "development"
    POSTGRES_URL: str = "postgresql://nexus_user:nexus_password@localhost:5432/nexuspay_db"
    
    # AWS SQS Config
    AWS_REGION: str = "us-east-1"
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    SQS_QUEUE_URL: str = "http://localhost:4566/000000000000/transacoes-events"

settings = Settings()
