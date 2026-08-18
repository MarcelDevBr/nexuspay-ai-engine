import pytest
from src.services.model_router import model_router
from src.services.rag_service import rag_service

def test_smart_model_router_light():
    route = model_router.route_request("Qual a taxa da maquininha?")
    assert route["tier"] == "LIGHT_MODEL"
    assert "llama3" in route["selected_model"]

def test_smart_model_router_heavy():
    route = model_router.route_request("Auditar divergência e contestação de chargeback com parecer BACEN")
    assert route["tier"] == "HEAVY_REASONING_MODEL"
    assert "claude" in route["selected_model"]

def test_generate_embedding():
    emb = rag_service.generate_embedding("taxa antecipacao")
    assert len(emb) == 1536
