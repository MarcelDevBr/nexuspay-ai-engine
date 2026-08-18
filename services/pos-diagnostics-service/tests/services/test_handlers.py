from src.services.handlers import (
    CryptoKeyDiagnosticHandler,
    EmvChipDiagnosticHandler,
    ConnectivityDiagnosticHandler,
    GenericDiagnosticHandler,
    PosDiagnosticsEngine,
    diagnostics_engine
)
from src.domain.models import ErrorCode

def test_crypto_key_handler():
    handler = CryptoKeyDiagnosticHandler()
    assert handler.can_handle(ErrorCode.CRYPTO_KEY_ERROR, "") is True
    assert handler.can_handle(None, "Erro de chave pinpad") is True
    assert handler.can_handle(None, "Falha de criptografia") is True
    assert handler.can_handle("OUTRO", "Sem relação") is False

    result = handler.execute("POS_001", ErrorCode.CRYPTO_KEY_ERROR, "Chave expirada")
    assert result.status == "RESOLVED"
    assert "reset_pos_security_keys" in result.action_taken

def test_emv_chip_handler():
    handler = EmvChipDiagnosticHandler()
    assert handler.can_handle(ErrorCode.EMV_CHIP_ERROR, "") is True
    assert handler.can_handle(None, "Falha de leitura do chip") is True
    assert handler.can_handle("OUTRO", "Sem relação") is False

    result = handler.execute("POS_002", ErrorCode.EMV_CHIP_ERROR, "Chip não lido")
    assert result.status == "RESOLVED"
    assert "calibrate_chip_reader_sensor" in result.action_taken

def test_connectivity_handler():
    handler = ConnectivityDiagnosticHandler()
    assert handler.can_handle(ErrorCode.CONNECTIVITY_TIMEOUT, "") is True
    assert handler.can_handle(None, "Sem sinal 4G ou rede wifi") is True
    assert handler.can_handle("OUTRO", "Sem relação") is False

    result = handler.execute("POS_003", ErrorCode.CONNECTIVITY_TIMEOUT, "Sem sinal")
    assert result.status == "RESOLVED"
    assert "check_telemetry_connectivity" in result.action_taken

def test_generic_handler():
    handler = GenericDiagnosticHandler()
    assert handler.can_handle("QUALQUER", "Qualquer erro") is True

    result = handler.execute("POS_004", "ERR_DESCONHECIDO", "Mensagem estranha")
    assert result.status == "RESOLVED"
    assert "perform_general_healthcheck" in result.action_taken

def test_pos_diagnostics_engine_custom_strategies():
    custom_engine = PosDiagnosticsEngine(strategies=[])
    result = custom_engine.diagnose("POS_005", "CODE", "Desc")
    assert result.status == "RESOLVED"
    assert "perform_general_healthcheck" in result.action_taken

def test_singleton_diagnostics_engine():
    assert diagnostics_engine is not None
    assert isinstance(diagnostics_engine, PosDiagnosticsEngine)
