import json
import numpy as np
from unittest.mock import MagicMock, patch
from src.services.semantic_cache import SemanticCacheService, semantic_cache_service

def test_cosine_similarity_calculation():
    cache = SemanticCacheService()
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    v3 = np.array([0.0, 1.0, 0.0])
    v_zero = np.array([0.0, 0.0, 0.0])

    assert cache._cosine_similarity(v1, v2) == 1.0
    assert cache._cosine_similarity(v1, v3) == 0.0
    assert cache._cosine_similarity(v1, v_zero) == 0.0

def test_semantic_cache_get_and_set_with_mock_redis():
    cache = SemanticCacheService()
    mock_redis = MagicMock()
    cache.redis_client = mock_redis

    # Simular set
    cache.set("pergunta teste", [1.0, 0.0], "resposta em cache", ttl_seconds=300)
    mock_redis.setex.assert_called_once()

    # Simular get com match
    cached_payload = json.dumps({
        "query": "pergunta teste",
        "embedding": [1.0, 0.0],
        "response": "resposta em cache"
    }).encode("utf-8")

    mock_redis.keys.return_value = [b"sem_cache:12345"]
    mock_redis.get.return_value = cached_payload

    result = cache.get([1.0, 0.0], threshold=0.9)
    assert result is not None
    response_text, sim = result
    assert response_text == "resposta em cache"
    assert sim >= 0.9

def test_semantic_cache_get_no_match():
    cache = SemanticCacheService()
    mock_redis = MagicMock()
    cache.redis_client = mock_redis

    cached_payload = json.dumps({
        "query": "outra pergunta",
        "embedding": [0.0, 1.0],
        "response": "outra resposta"
    }).encode("utf-8")

    mock_redis.keys.return_value = [b"sem_cache:123"]
    mock_redis.get.return_value = cached_payload

    result = cache.get([1.0, 0.0], threshold=0.9)
    assert result is None

def test_semantic_cache_empty_keys_and_empty_raw_data():
    cache = SemanticCacheService()
    mock_redis = MagicMock()
    cache.redis_client = mock_redis

    # Sem chaves
    mock_redis.keys.return_value = []
    assert cache.get([1.0, 0.0]) is None

    # Chave sem dados brutos
    mock_redis.keys.return_value = [b"sem_cache:123"]
    mock_redis.get.return_value = None
    assert cache.get([1.0, 0.0]) is None

def test_semantic_cache_handles_none_client():
    cache = SemanticCacheService()
    cache.redis_client = None
    assert cache.get([1.0, 0.0]) is None
    cache.set("teste", [1.0], "resp") # Não deve levantar exceção

def test_semantic_cache_handles_redis_exceptions():
    cache = SemanticCacheService()
    mock_redis = MagicMock()
    mock_redis.keys.side_effect = Exception("Redis error")
    mock_redis.setex.side_effect = Exception("Redis write error")
    cache.redis_client = mock_redis

    assert cache.get([1.0, 0.0]) is None
    cache.set("teste", [1.0], "resp") # Deve capturar logar e não crashar

def test_semantic_cache_init_failure():
    with patch("redis.Redis.from_url", side_effect=Exception("Connection failed")):
        failed_cache = SemanticCacheService()
        assert failed_cache.redis_client is None

def test_singleton_semantic_cache():
    assert semantic_cache_service is not None
    assert isinstance(semantic_cache_service, SemanticCacheService)
