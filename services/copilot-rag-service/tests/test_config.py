from src.config import Settings, settings

def test_settings_initialization_and_defaults():
    s = Settings()
    assert s.ENV in ["development", "test", "production"]
    assert "postgresql://" in s.POSTGRES_URL
    assert "redis://" in s.REDIS_URL
    assert s.AWS_REGION == "us-east-1"
    assert s.USE_MOCK_LLM is True
    assert s.MAX_TOKENS_PER_REQUEST == 1000

def test_singleton_settings_instance():
    assert settings is not None
    assert isinstance(settings, Settings)
