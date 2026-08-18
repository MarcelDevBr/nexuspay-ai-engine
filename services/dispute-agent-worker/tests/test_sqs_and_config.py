import pytest
from unittest.mock import MagicMock, patch
from src.config import Settings
from src.workers.sqs_consumer import SqsEventConsumer

def test_settings_initialization():
    settings = Settings()
    assert settings.ENV == "development"
    assert "transacoes-events" in settings.SQS_QUEUE_URL

def test_sqs_consumer_get_client():
    consumer = SqsEventConsumer()
    client = consumer.get_sqs_client()
    assert client is not None

def test_sqs_consumer_stop():
    consumer = SqsEventConsumer()
    consumer.is_running = True
    consumer.stop_polling()
    assert consumer.is_running is False
