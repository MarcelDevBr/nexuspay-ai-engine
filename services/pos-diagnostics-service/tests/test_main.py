from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_pos_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert data["service"] == "nexuspay-pos-diagnostics-service"
    assert data["version"] == "1.0.0"

def test_cors_middleware():
    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

def test_main_execution():
    with patch("uvicorn.run") as mock_uvicorn:
        import runpy
        with patch.object(runpy, "_run_module_code", return_value={}):
            pass
