import pytest
from src.services.handlers import (
    CryptoKeyDiagnosticHandler,
    EmvChipDiagnosticHandler,
    ConnectivityDiagnosticHandler,
    GenericDiagnosticHandler,
    PosDiagnosticsEngine
)
from src.domain.models import ErrorCode
from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_crypto_key_handler_by_error_code():
    handler = CryptoKeyDiagnosticHandler()
    assert handler.can_handle(ErrorCode.CRYPTO_KEY_ERROR, "qualquer texto") is True
    res = handler.execute("POS_1", ErrorCode.CRYPTO_KEY_ERROR, "falha")
    assert "reset_pos_security_keys" in res.action_taken
    assert res.status == "RESOLVED"

def test_crypto_key_handler_by_keyword():
    handler = CryptoKeyDiagnosticHandler()
    assert handler.can_handle(None, "problema com pinpad e chave de segurança") is True

def test_emv_chip_handler():
    handler = EmvChipDiagnosticHandler()
    assert handler.can_handle(ErrorCode.EMV_CHIP_ERROR, "") is True
    assert handler.can_handle(None, "leitura do chip falhou") is True
    res = handler.execute("POS_2", ErrorCode.EMV_CHIP_ERROR, "")
    assert "calibrate_chip_reader_sensor" in res.action_taken

def test_connectivity_handler():
    handler = ConnectivityDiagnosticHandler()
    assert handler.can_handle(ErrorCode.CONNECTIVITY_TIMEOUT, "") is True
    assert handler.can_handle(None, "sinal 4g fraco") is True
    assert handler.can_handle(None, "conexao wifi instavel") is True
    res = handler.execute("POS_3", ErrorCode.CONNECTIVITY_TIMEOUT, "")
    assert "check_telemetry_connectivity" in res.action_taken

def test_generic_handler():
    handler = GenericDiagnosticHandler()
    assert handler.can_handle(None, "erro desconhecido") is True
    res = handler.execute("POS_4", None, "erro desconhecido")
    assert "perform_general_healthcheck" in res.action_taken

def test_pos_diagnostics_engine_custom_strategy():
    engine = PosDiagnosticsEngine(strategies=[GenericDiagnosticHandler()])
    res = engine.diagnose("POS_5", "QUALQUER", "texto")
    assert res.status == "RESOLVED"

def test_api_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"

def test_api_diagnosis_endpoint():
    response = client.post("/api/v1/diagnosis/pos", json={
        "terminal_id": "POS_STONE_777",
        "error_code": "ERR_58",
        "description": "chave expirada"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["terminal_id"] == "POS_STONE_777"
    assert "reset_pos_security_keys" in data["action_taken"]
