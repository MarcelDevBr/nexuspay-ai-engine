import pytest
import runpy
from unittest.mock import patch, MagicMock
from src.ports.agent_ports import IEvidenceExtractorAgent, IComplianceAuditorAgent, ILegalDefenseAgent
from src.workers.kafka_consumer import KafkaEventConsumer

def test_abstract_agent_ports():
    assert IEvidenceExtractorAgent.extract_evidence(None, "tx-1", "loj-1") is None
    assert IComplianceAuditorAgent.audit_compliance(None, None, "motivo") is None
    assert ILegalDefenseAgent.generate_defense_dossier(None, "tx-1", "loj-1", "motivo", None, None) is None

def test_kafka_consumer_invalid_payload():
    consumer = KafkaEventConsumer()
    res = consumer.process_message_payload("invalid json {")
    assert res is None

@pytest.mark.asyncio
async def test_main_execution():
    with patch("src.workers.sqs_consumer.sqs_consumer.start_polling") as mock_poll:
        # Test normal main execution
        from src.main import main
        await main()
        mock_poll.assert_called_once()

@pytest.mark.asyncio
async def test_main_keyboard_interrupt():
    with patch("src.workers.sqs_consumer.sqs_consumer.start_polling", side_effect=KeyboardInterrupt):
        with patch("src.workers.sqs_consumer.sqs_consumer.stop_polling") as mock_stop:
            from src.main import main
            await main()
            mock_stop.assert_called_once()

def test_main_module_run():
    with patch("asyncio.run") as mock_async_run:
        runpy.run_module("src.main", run_name="__main__")
        mock_async_run.assert_called_once()
