import json
import asyncio
import pytest
from src.workers.kafka_consumer import KafkaEventConsumer, kafka_consumer

def test_process_message_payload_high_value():
    consumer = KafkaEventConsumer()
    payload = json.dumps({
        "transacaoId": "tx_kafka_999",
        "lojistaId": "loj_kafka_123",
        "valor": 1250.00
    })

    result = consumer.process_message_payload(payload)
    assert result is not None
    assert result.transacao_id == "tx_kafka_999"
    assert result.status == "DEFENDIDO_AUTOMATICAMENTE"

def test_process_message_payload_low_value():
    consumer = KafkaEventConsumer()
    payload = json.dumps({
        "transacaoId": "tx_kafka_low",
        "lojistaId": "loj_kafka_123",
        "valor": 50.00
    })

    result = consumer.process_message_payload(payload)
    assert result is None

def test_process_message_payload_invalid_json():
    consumer = KafkaEventConsumer()
    result = consumer.process_message_payload("invalid-json")
    assert result is None

@pytest.mark.asyncio
async def test_kafka_consumer_loop_start_and_stop():
    consumer = KafkaEventConsumer()
    loop_task = asyncio.create_task(consumer.start_consumer_loop())
    await asyncio.sleep(0.01)
    assert consumer.is_running is True
    consumer.stop_consumer_loop()
    await loop_task
    assert consumer.is_running is False

def test_singleton_kafka_consumer():
    assert kafka_consumer is not None
    assert isinstance(kafka_consumer, KafkaEventConsumer)
