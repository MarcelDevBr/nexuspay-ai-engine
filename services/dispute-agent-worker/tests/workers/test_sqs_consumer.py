import json
import asyncio
import pytest
from unittest.mock import MagicMock, patch
from src.workers.sqs_consumer import SqsEventConsumer, sqs_consumer

def test_sqs_client_creation():
    consumer = SqsEventConsumer()
    client = consumer.get_sqs_client()
    assert client is not None

@pytest.mark.asyncio
async def test_sqs_consumer_polling_with_messages():
    consumer = SqsEventConsumer()
    mock_sqs = MagicMock()
    
    msg_high = {
        "Body": json.dumps({"transacaoId": "tx_sqs_1", "lojistaId": "loj_1", "valor": 800.00}),
        "ReceiptHandle": "receipt_1"
    }
    msg_low = {
        "Body": json.dumps({"transacaoId": "tx_sqs_2", "lojistaId": "loj_2", "valor": 100.00}),
        "ReceiptHandle": "receipt_2"
    }

    def side_effect_receive(**kwargs):
        consumer.stop_polling()
        return {"Messages": [msg_high, msg_low]}

    mock_sqs.receive_message.side_effect = side_effect_receive

    with patch.object(consumer, "get_sqs_client", return_value=mock_sqs):
        await consumer.start_polling()
        assert mock_sqs.delete_message.call_count == 2
        assert consumer.is_running is False

@pytest.mark.asyncio
async def test_sqs_consumer_polling_exception_handling():
    consumer = SqsEventConsumer()
    mock_sqs = MagicMock()

    def side_effect_error(**kwargs):
        consumer.stop_polling()
        raise Exception("SQS network error")

    mock_sqs.receive_message.side_effect = side_effect_error

    with patch.object(consumer, "get_sqs_client", return_value=mock_sqs), \
         patch("asyncio.sleep") as mock_sleep:
        mock_sleep.return_value = None
        await consumer.start_polling()
        assert consumer.is_running is False

def test_singleton_sqs_consumer():
    assert sqs_consumer is not None
    assert isinstance(sqs_consumer, SqsEventConsumer)
