import io
import json
import pytest
import runpy
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import numpy as np

from src.main import app
from src.services.rag_service import RAGService
from src.services.semantic_cache import SemanticCacheService

client = TestClient(app)

def test_api_chat_stream():
    response = client.post("/api/v1/chat/stream", json={"lojista_id": "loj-1", "prompt": "Como funciona antecipação?"})
    assert response.status_code == 200
    assert "data:" in response.text

def test_api_chat_route():
    response = client.post("/api/v1/chat/route", json={"lojista_id": "loj-1", "prompt": "Explique a regra BACEN"})
    assert response.status_code == 200
    data = response.json()
    assert "tier" in data

def test_main_execution():
    with patch("uvicorn.run") as mock_run:
        runpy.run_module("src.main", run_name="__main__")
        mock_run.assert_called_once()

def test_bedrock_embedding_generation():
    with patch("src.config.settings.USE_MOCK_LLM", False):
        with patch("boto3.client") as mock_boto:
            mock_bedrock = MagicMock()
            mock_boto.return_value = mock_bedrock
            
            fake_body = io.BytesIO(json.dumps({"embedding": [0.1] * 1536}).encode("utf-8"))
            mock_bedrock.invoke_model.return_value = {"body": fake_body}
            
            svc = RAGService()
            vec = svc.generate_embedding("teste de prompt")
            assert len(vec) == 1536
            assert vec[0] == 0.1

def test_semantic_cache_edge_cases():
    svc = SemanticCacheService()
    # Test zero vectors
    assert svc._cosine_similarity(np.zeros(10), np.zeros(10)) == 0.0

    # Test init failure
    with patch("redis.Redis.from_url", side_effect=Exception("Redis offline")):
        failed_svc = SemanticCacheService()
        assert failed_svc.redis_client is None
        assert failed_svc.get([0.1]) is None
        failed_svc.set("query", [0.1], "resp")

    # Test get with none raw_data, low similarity, and exception
    mock_redis = MagicMock()
    svc.redis_client = mock_redis
    
    # 1. key returns None
    mock_redis.keys.return_value = ["sem_cache:1", "sem_cache:2"]
    mock_redis.get.side_effect = [None, json.dumps({"embedding": [1.0] * 1536, "response": "resp"}).encode("utf-8")]
    res = svc.get([0.0] * 1536, threshold=0.99)
    assert res is None

    # 2. exception in get
    mock_redis.keys.side_effect = Exception("Redis error")
    assert svc.get([0.1]) is None

    # 3. exception in set
    mock_redis.setex.side_effect = Exception("Set error")
    svc.set("prompt", [0.1], "resp")

@pytest.mark.asyncio
async def test_stream_copilot_response_miss_and_hit():
    svc = RAGService()
    # 1. First call (cache miss)
    chunks = []
    async for chunk in svc.stream_copilot_response("loj_123", "Pergunta inédita sobre taxas de maquininha"):
        chunks.append(chunk)
    assert len(chunks) > 0

    # 2. Second call with simulated cache hit
    with patch("src.services.semantic_cache.semantic_cache_service.get", return_value=("Resposta em Cache", 0.95)):
        hit_chunks = []
        async for chunk in svc.stream_copilot_response("loj_123", "Pergunta idêntica"):
            hit_chunks.append(chunk)
        assert any("Cache Semântico" in c for c in hit_chunks)
