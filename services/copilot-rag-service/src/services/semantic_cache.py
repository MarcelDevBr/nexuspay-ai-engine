import json
import logging
from typing import Optional, Tuple
import numpy as np
import redis
from src.config import settings

logger = logging.getLogger("nexuspay.semantic_cache")

class SemanticCacheService:
    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=False)
        except Exception as e:
            logger.warning(f"Não foi possível conectar ao Redis: {e}.")
            self.redis_client = None

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(dot_product / (norm_v1 * norm_v2))

    def get(self, query_embedding: list[float], threshold: float = 0.92) -> Optional[Tuple[str, float]]:
        if not self.redis_client:
            return None

        try:
            keys = self.redis_client.keys("sem_cache:*")
            if not keys:
                return None

            q_vec = np.array(query_embedding, dtype=np.float32)

            for key in keys:
                raw_data = self.redis_client.get(key)
                if not raw_data:
                    continue
                data = json.loads(raw_data.decode("utf-8"))
                cached_vec = np.array(data["embedding"], dtype=np.float32)
                sim = self._cosine_similarity(q_vec, cached_vec)

                if sim >= threshold:
                    logger.info(f"⚡ [SEMANTIC CACHE HIT] Similaridade: {sim:.4f} >= {threshold}. Latência: ~10ms / R$ 0,00")
                    return data["response"], sim

            return None
        except Exception as e:
            logger.error(f"Erro ao buscar no Semantic Cache: {e}")
            return None

    def set(self, query_text: str, query_embedding: list[float], response: str, ttl_seconds: int = 3600):
        if not self.redis_client:
            return

        try:
            cache_id = f"sem_cache:{abs(hash(query_text))}"
            payload = {
                "query": query_text,
                "embedding": query_embedding,
                "response": response
            }
            self.redis_client.setex(cache_id, ttl_seconds, json.dumps(payload))
            logger.info(f"Gravado no Semantic Cache: {cache_id}")
        except Exception as e:
            logger.error(f"Erro ao gravar no Semantic Cache: {e}")

semantic_cache_service = SemanticCacheService()
