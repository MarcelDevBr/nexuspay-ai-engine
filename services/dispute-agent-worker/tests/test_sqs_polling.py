import pytest
import asyncio
from unittest.mock import MagicMock, patch
from src.workers.sqs_consumer import SqsEventConsumer

@pytest.mark.asyncio
async def test_sqs_polling_with_high_value_transaction():
    consumer = SqsEventConsumer()
    mock_sqs = MagicMock()
    mock_sqs.receive_message.side_effect = [
        {
            "Messages": [
                {
                    "Body": '{"transacaoId": "tx-999", "lojistaId": "lojista-1", "valor": 750.00}',
                    "ReceiptHandle": "receipt-123"
                }
            ]
        },
        Exception("Stop polling for test")
    ]
    
    with patch.object(consumer, "get_sqs_client", return_value=mock_sqs):
        with patch("src.agents.dispute_crew.dispute_crew.process_chargeback_dispute") as mock_dispute:
            # Roda 1 ciclo de polling
            task = asyncio.create_task(consumer.start_polling())
            await asyncio.sleep(0.05)
            consumer.stop_polling()
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass
            
            mock_dispute.assert_called_once_with(
                transacao_id="tx-999",
                lojista_id="lojista-1",
                motivo="Auditoria Preventiva de Risco e Fraude"
            )
            mock_sqs.delete_message.assert_called_once()
