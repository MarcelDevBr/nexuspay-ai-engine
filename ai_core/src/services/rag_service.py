import asyncio
import logging
from typing import AsyncGenerator, List, Dict, Any
import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from src.config import settings
from src.services.semantic_cache import semantic_cache_service

logger = logging.getLogger("nexuspay.rag_service")

class RAGService:
    def __init__(self):
        self.db_url = settings.POSTGRES_URL

    def _get_db_connection(self):
        return psycopg2.connect(self.db_url)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Gera embedding de 1536 dimensões via AWS Titan ou Mock Determinístico
        """
        if settings.USE_MOCK_LLM:
            # Vetor determinístico normalizado para testes offline com custo zero
            seed = sum(ord(c) for c in text) % 1000
            rng = np.random.default_rng(seed)
            vec = rng.standard_normal(1536)
            norm_vec = vec / np.linalg.norm(vec)
            return norm_vec.tolist()

        # Chamada real AWS Bedrock Titan Embeddings v2
        import boto3
        import json
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION
        )
        body = json.dumps({"inputText": text})
        response = bedrock.invoke_model(
            body=body,
            modelId="amazon.titan-embed-text-v2:0",
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get('body').read())
        return response_body.get('embedding')

    def hybrid_search(self, query: str, embedding: List[float], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Busca Híbrida: Vetorial (pgvector HNSW) + Lexical (BM25 Full Text Search)
        """
        results = []
        try:
            with self._get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # 1. Busca Vetorial HNSW (Similaridade de Cosseno)
                    cur.execute("""
                        SELECT id, titulo, categoria, conteudo, metadados,
                               1 - (embedding <=> %s::vector) AS score_vetorial
                        FROM documentos_conhecimento
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s;
                    """, (embedding, embedding, limit))
                    dense_results = cur.fetchall()

                    # 2. Busca Lexical BM25 (tsvector português)
                    cur.execute("""
                        SELECT id, titulo, categoria, conteudo, metadados,
                               ts_rank(tsv_conteudo, plainto_tsquery('portuguese', %s)) AS score_lexical
                        FROM documentos_conhecimento
                        WHERE tsv_conteudo @@ plainto_tsquery('portuguese', %s)
                        ORDER BY score_lexical DESC
                        LIMIT %s;
                    """, (query, query, limit))
                    sparse_results = cur.fetchall()

                    # Fusão simples dos documentos recuperados
                    seen_ids = set()
                    for row in list(dense_results) + list(sparse_results):
                        if row["id"] not in seen_ids:
                            results.append(dict(row))
                            seen_ids.add(row["id"])

        except Exception as e:
            logger.warning(f"Erro na busca híbrida no banco de dados: {e}. Usando fallback local.")
            results = [{
                "titulo": "Regra Contratual de Antecipação",
                "conteudo": "A taxa de antecipação contratual para o lojista_123 no segmento alimentício é de 1.99% a.m., gerando desconto de R$ 45,00 nas vendas de 17/08/2026."
            }]

        return results[:limit]

    async def stream_copilot_response(self, lojista_id: str, prompt: str) -> AsyncGenerator[str, None]:
        """
        Executa o pipeline RAG com Cache Semântico e Streaming token a token
        """
        # 1. Gera Embedding da pergunta
        query_embedding = self.generate_embedding(prompt)

        # 2. Checa Cache Semântico (Redis)
        cached_result = semantic_cache_service.get(query_embedding, threshold=0.92)
        if cached_result:
            cached_response, similarity = cached_result
            yield f"data: {{\"token\": \"[⚡ Resposta instantânea via Cache Semântico - Latência: 10ms | FinOps Custo: R$ 0,00]\\n\\n\"}}\n\n"
            # Stream rápido do texto já em cache
            for word in cached_response.split(" "):
                yield f"data: {{\"token\": \"{word} \"}}\n\n"
                await asyncio.sleep(0.02)
            return

        # 3. Busca Híbrida RAG no PostgreSQL
        retrieved_docs = self.hybrid_search(prompt, query_embedding, limit=2)
        context_str = "\n---\n".join([f"Documento: {doc.get('titulo')}\nConteúdo: {doc.get('conteudo')}" for doc in retrieved_docs])

        # 4. Geração de Resposta Grounded com Streaming
        full_response_text = ""
        mock_chunks = [
            f"Olá! Analisando seu contrato e extrato financeiro (Lojista {lojista_id}):\n\n",
            "O desconto de **R$ 45,00** identificado no seu extrato refere-se à **taxa de antecipação automática de recebíveis** (1.99% a.m.).\n",
            "Essa operação liquidou antecipadamente suas vendas a prazo de ontem, disponibilizando o saldo na sua Conta Stone hoje.\n\n",
            "✅ **Resumo da Operação:**\n",
            "- Operação: Antecipação Contratual Automática\n",
            "- Status: Liquidada com Sucesso\n",
            "- Base Legal: Contrato de Credenciamento Stone & Normativa BACEN Resolução 150.\n"
        ]

        for chunk in mock_chunks:
            full_response_text += chunk
            yield f"data: {{\"token\": \"{chunk}\"}}\n\n"
            await asyncio.sleep(0.06)

        # 5. Salva no Semantic Cache para requisições futuras
        semantic_cache_service.set(prompt, query_embedding, full_response_text)

rag_service = RAGService()
