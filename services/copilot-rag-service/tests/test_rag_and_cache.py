import pytest
import numpy as np
from src.services.semantic_cache import SemanticCacheService
from src.services.rag_service import RAGService

def test_semantic_cache_cosine_similarity():
    cache = SemanticCacheService()
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    assert cache._cosine_similarity(v1, v2) == 1.0

    v3 = np.array([0.0, 1.0, 0.0])
    assert cache._cosine_similarity(v1, v3) == 0.0

    v_zero = np.array([0.0, 0.0, 0.0])
    assert cache._cosine_similarity(v1, v_zero) == 0.0

def test_semantic_cache_get_and_set_without_redis():
    cache = SemanticCacheService()
    cache.redis_client = None
    assert cache.get([0.1] * 1536) is None
    cache.set("pergunta", [0.1] * 1536, "resposta")

def test_rag_hybrid_search_fallback():
    rag = RAGService()
    rag.db_url = "postgresql://invalido:invalido@localhost:9999/invalido"
    results = rag.hybrid_search("taxa de antecipação", [0.1] * 1536, limit=2)
    assert len(results) >= 1
    assert "Regra Contratual" in results[0]["titulo"]

@pytest.mark.asyncio
async def test_stream_copilot_response():
    rag = RAGService()
    rag.db_url = "postgresql://invalido:invalido@localhost:9999/invalido"
    chunks = []
    async for chunk in rag.stream_copilot_response("lojista_123", "Qual minha taxa?"):
        chunks.append(chunk)
    assert len(chunks) > 0
    full_output = "".join(chunks)
    assert "antecipação" in full_output or "taxa" in full_output
