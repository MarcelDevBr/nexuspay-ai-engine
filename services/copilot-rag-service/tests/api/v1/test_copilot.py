from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat_route_endpoint_simple_query():
    payload = {
        "lojista_id": "lojista_123",
        "prompt": "Como vejo minhas vendas de ontem?"
    }
    response = client.post("/api/v1/chat/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tier"] == "LIGHT_MODEL"
    assert data["is_complex"] is False
    assert "llama3" in data["selected_model"]

def test_chat_route_endpoint_complex_query():
    payload = {
        "lojista_id": "lojista_123",
        "prompt": "Gostaria de abrir uma disputa de chargeback por suspeita de fraude na transação."
    }
    response = client.post("/api/v1/chat/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tier"] == "HEAVY_REASONING_MODEL"
    assert data["is_complex"] is True
    assert "claude-3-5-sonnet" in data["selected_model"]

def test_chat_stream_endpoint():
    payload = {
        "lojista_id": "lojista_123",
        "prompt": "Explique a taxa de R$ 45 no meu extrato"
    }
    response = client.post("/api/v1/chat/stream", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert len(response.text) > 0
    assert "data:" in response.text
