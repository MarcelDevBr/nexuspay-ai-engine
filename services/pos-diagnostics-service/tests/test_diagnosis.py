import pytest
from src.api.v1.diagnosis import diagnose_pos, PosDiagnosisRequest

@pytest.mark.asyncio
async def test_diagnose_pos_crypto_key_error():
    req = PosDiagnosisRequest(
        terminal_id="POS_STONE_123",
        error_code="ERR_58",
        description="Erro de chave criptográfica na tela"
    )
    res = await diagnose_pos(req)
    assert res.status == "RESOLVED"
    assert "reset_pos_security_keys" in res.action_taken
    assert "chaves de segurança" in res.instrucoes_lojista

@pytest.mark.asyncio
async def test_diagnose_pos_telemetry_error():
    req = PosDiagnosisRequest(
        terminal_id="POS_STONE_456",
        description="Sinal fraco ou sem conexão"
    )
    res = await diagnose_pos(req)
    assert res.status == "RESOLVED"
    assert "check_telemetry_connectivity" in res.action_taken
