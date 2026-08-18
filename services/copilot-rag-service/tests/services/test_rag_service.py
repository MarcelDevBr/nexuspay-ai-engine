import pytest
from unittest.mock import patch, MagicMock
from src.services.rag_service import RAGService, rag_service
from src.config import settings

def test_generate_embedding_mock():
    rag = RAGService()
    emb = rag.generate_embedding("Taxa de antecipação Stone")
    assert isinstance(emb, list)
    assert len(emb) == 1536
    assert abs(sum(x*x for x in emb) - 1.0) < 1e-4

def test_generate_embedding_aws_bedrock():
    with patch.object(settings, "USE_MOCK_LLM", False):
        with patch("boto3.client") as mock_boto:
            mock_client = MagicMock()
            mock_boto.return_value = mock_client
            
            mock_body = MagicMock()
            mock_body.read.return_value = b'{"embedding": [0.1, 0.2, 0.3]}'
            mock_client.invoke_model.return_value = {"body": mock_body}
            
            rag = RAGService()
            emb = rag.generate_embedding("Texto teste")
            assert emb == [0.1, 0.2, 0.3]

def test_get_db_connection():
    rag = RAGService()
    with patch("psycopg2.connect") as mock_conn:
        mock_conn.return_value = MagicMock()
        conn = rag._get_db_connection()
        assert conn is not None
        mock_conn.assert_called_once_with(rag.db_url)

def test_hybrid_search_with_mocked_database_success():
    rag = RAGService()
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    dense_row = {"id": 1, "titulo": "Doc 1", "categoria": "Taxas", "conteudo": "Tx", "metadados": {}}
    sparse_row = {"id": 2, "titulo": "Doc 2", "categoria": "POS", "conteudo": "POS", "metadados": {}}
    mock_cur.fetchall.side_effect = [[dense_row], [sparse_row]]

    with patch.object(rag, "_get_db_connection", return_value=mock_conn):
        results = rag.hybrid_search("taxa", [0.1]*1536, limit=2)
        assert len(results) == 2
        assert results[0]["titulo"] == "Doc 1"
        assert results[1]["titulo"] == "Doc 2"

def test_hybrid_search_fallback_on_exception():
    rag = RAGService()
    with patch.object(rag, "_get_db_connection", side_effect=Exception("DB connection error")):
        results = rag.hybrid_search("antecipação", [0.1]*1536, limit=3)
        assert len(results) >= 1
        assert "Regra Contratual" in results[0]["titulo"]

@pytest.mark.asyncio
async def test_stream_copilot_response_cache_miss():
    rag = RAGService()
    with patch("src.services.rag_service.semantic_cache_service.get", return_value=None), \
         patch("src.services.rag_service.semantic_cache_service.set") as mock_set:
        chunks = []
        async for chunk in rag.stream_copilot_response("lojista_999", "Consulta inédita sem cache"):
            chunks.append(chunk)
        
        full_text = "".join(chunks)
        assert "lojista_999" in full_text
        assert "R$ 45,00" in full_text
        mock_set.assert_called_once()

@pytest.mark.asyncio
async def test_stream_copilot_response_cache_hit():
    rag = RAGService()
    cached_payload = ("Esta é uma resposta em cache", 0.98)
    with patch("src.services.rag_service.semantic_cache_service.get", return_value=cached_payload):
        chunks = []
        async for chunk in rag.stream_copilot_response("lojista_999", "Consulta já em cache"):
            chunks.append(chunk)
        
        full_text = "".join(chunks)
        assert "Cache Semântico" in full_text
        assert "resposta" in full_text

def test_singleton_rag_service():
    assert rag_service is not None
    assert isinstance(rag_service, RAGService)
