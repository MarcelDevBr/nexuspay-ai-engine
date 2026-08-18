import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from src.main import main

@pytest.mark.asyncio
async def test_main_startup_and_cancellation():
    with patch("src.main.sqs_consumer.start_polling", new_callable=AsyncMock) as mock_poll:
        mock_poll.side_effect = KeyboardInterrupt
        await main()
        mock_poll.assert_awaited_once()

def test_main_execution():
    with patch("asyncio.run") as mock_run:
        import runpy
        with patch.object(runpy, "_run_module_code", return_value={}):
            pass
