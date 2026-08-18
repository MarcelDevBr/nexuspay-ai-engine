import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.rag_service import RAGService
from src.services.semantic_cache import SemanticCacheService
from unittest.mock import MagicMock, patch

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert data["service"] == "nexuspay-copilot-rag-service"

def test_rag_service_hybrid_search_with_mock():
    with patch.object(RAGService, "_get_db_connection") as mock_db:
        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [{"id": "doc1", "titulo": "Taxa de Antecipação", "categoria": "contrato", "conteudo": "1.99%", "metadados": {}}],
            [{"id": "doc2", "titulo": "Termos de Uso", "categoria": "termos", "conteudo": "Geral", "metadados": {}}]
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_db.return_value.__enter__.return_value = mock_conn
        
        service = RAGService()
        emb = service.generate_embedding("como funciona a antecipação?")
        results = service.hybrid_search("como funciona a antecipação?", emb, limit=2)
        assert len(results) >= 1

def test_semantic_cache_redis_integration():
    mock_redis = MagicMock()
    mock_redis.keys.return_value = []
    
    cache = SemanticCacheService()
    cache.redis_client = mock_redis
    
    emb = [0.1] * 1536
    res = cache.get(emb, threshold=0.9)
    assert res is None
    
    cache.set("pergunta teste", emb, "resposta teste")
    mock_redis.setex.assert_called_once()
