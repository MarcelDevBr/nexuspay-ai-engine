import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock
from src.workers.kafka_consumer import KafkaEventConsumer

def test_kafka_consumer_process_high_value_transaction():
    consumer = KafkaEventConsumer()
    payload = json.dumps({
        "transacaoId": "tx-kafka-777",
        "lojistaId": "lojista-digital-88",
        "valor": 1250.00
    })

    with patch("src.agents.dispute_crew.dispute_crew.process_chargeback_dispute") as mock_dispute:
        mock_dispute.return_value = {"status": "SUCCESS", "defesa": "Defesa gerada"}
        res = consumer.process_message_payload(payload)
        
        mock_dispute.assert_called_once_with(
            transacao_id="tx-kafka-777",
            lojista_id="lojista-digital-88",
            motivo="Auditoria Preventiva Kafka Stream - Análise de Fraude em Tempo Real"
        )
        assert res is not None

def test_kafka_consumer_process_low_value_transaction():
    consumer = KafkaEventConsumer()
    payload = json.dumps({
        "transacaoId": "tx-kafka-123",
        "lojistaId": "lojista-digital-88",
        "valor": 45.00
    })

    with patch("src.agents.dispute_crew.dispute_crew.process_chargeback_dispute") as mock_dispute:
        res = consumer.process_message_payload(payload)
        mock_dispute.assert_not_called()
        assert res is None

@pytest.mark.asyncio
async def test_kafka_consumer_lifecycle():
    consumer = KafkaEventConsumer()
    task = asyncio.create_task(consumer.start_consumer_loop())
    await asyncio.sleep(0.02)
    consumer.stop_consumer_loop()
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass
    assert consumer.is_running is False
