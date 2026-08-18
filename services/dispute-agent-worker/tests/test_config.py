from src.config import Settings, settings

def test_settings_defaults():
    s = Settings()
    assert s.ENV in ["development", "test", "production"]
    assert "postgresql://" in s.POSTGRES_URL
    assert s.AWS_REGION == "us-east-1"
    assert "transacoes-events" in s.SQS_QUEUE_URL
    assert "nexuspay.transacoes.events" in s.KAFKA_TOPIC_TRANSACOES
    assert s.KAFKA_GROUP_ID == "nexuspay-dispute-worker-group"

def test_singleton_settings():
    assert settings is not None
    assert isinstance(settings, Settings)
