import pytest
from src.services.model_router import model_router
from src.agents.dispute_crew import dispute_crew
from src.services.rag_service import rag_service

def test_smart_model_router_light_prompt():
    prompt = "Qual o horário de atendimento da Stone?"
    route = model_router.route_request(prompt)
    assert route["tier"] == "LIGHT_MODEL"
    assert "llama3" in route["selected_model"]
    assert route["is_complex"] is False

def test_smart_model_router_heavy_prompt():
    prompt = "Preciso auditar uma divergência de conciliação e contestação de chargeback do BACEN"
    route = model_router.route_request(prompt)
    assert route["tier"] == "HEAVY_REASONING_MODEL"
    assert "claude" in route["selected_model"]
    assert route["is_complex"] is True

def test_dispute_crew_chargeback_generation():
    result = dispute_crew.process_chargeback_dispute(
        transacao_id="transacao_mock_123",
        lojista_id="lojista_123",
        motivo="Não reconhecimento de compra"
    )
    assert result["status"] == "DEFENDIDO_AUTOMATICAMENTE"
    assert result["score_probabilidade_ganho"] > 90.0
    assert "DOSSIÊ DE DEFESA" in result["dossie_defesa"]
    assert result["evidencias"]["chip_emv_lido"] is True

def test_rag_generate_embedding_deterministic():
    text = "taxa de antecipação"
    embedding = rag_service.generate_embedding(text)
    assert len(embedding) == 1536
    # Confirma que é normalizado (norma próxima de 1)
    import numpy as np
    norm = np.linalg.norm(embedding)
    assert pytest.approx(norm, 0.01) == 1.0
