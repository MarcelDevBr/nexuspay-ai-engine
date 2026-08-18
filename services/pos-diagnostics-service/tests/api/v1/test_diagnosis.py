from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_diagnose_pos_crypto_key_success():
    payload = {
        "terminal_id": "POS_STONE_888",
        "error_code": "ERR_58",
        "description": "Terminal travado pedindo reinicialização de chaves"
    }
    response = client.post("/api/v1/diagnosis/pos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["terminal_id"] == "POS_STONE_888"
    assert data["status"] == "RESOLVED"
    assert "reset_pos_security_keys" in data["action_taken"]
    assert "chaves de segurança" in data["instrucoes_lojista"]

def test_diagnose_pos_connectivity_success():
    payload = {
        "terminal_id": "POS_STONE_999",
        "error_code": "ERR_91",
        "description": "Sem sinal 4G para transacionar"
    }
    response = client.post("/api/v1/diagnosis/pos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["terminal_id"] == "POS_STONE_999"
    assert data["status"] == "RESOLVED"
    assert "check_telemetry_connectivity" in data["action_taken"]
