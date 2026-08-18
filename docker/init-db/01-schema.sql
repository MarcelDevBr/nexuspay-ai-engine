-- =============================================================================
-- NexusPay AI Engine - Database Schema (PostgreSQL 16 + pgvector)
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. Multi-Tenant Lojistas (Merchants)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lojistas (
    id VARCHAR(50) PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    cnpj_hash VARCHAR(64) NOT NULL UNIQUE,
    email_contato VARCHAR(150) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 2. Transações Particionadas por Mês (High Scale ACID Ledger)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transacoes (
    id UUID DEFAULT gen_random_uuid(),
    lojista_id VARCHAR(50) NOT NULL REFERENCES lojistas(id),
    terminal_id VARCHAR(50),
    valor NUMERIC(15, 2) NOT NULL,
    tipo VARCHAR(30) NOT NULL, -- PIX, CREDITO_A_VISTA, CREDITO_PARCELADO, DEBITO
    status VARCHAR(20) NOT NULL, -- AUTORIZADA, NEGADA, LIQUIDADA, EM_DISPUTA
    codigo_autorizacao VARCHAR(50),
    criado_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, criado_em)
) PARTITION BY RANGE (criado_em);

-- Criação das partições 2026
CREATE TABLE IF NOT EXISTS transacoes_2026_01 PARTITION OF transacoes
    FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2026-02-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_02 PARTITION OF transacoes
    FOR VALUES FROM ('2026-02-01 00:00:00+00') TO ('2026-03-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_03 PARTITION OF transacoes
    FOR VALUES FROM ('2026-03-01 00:00:00+00') TO ('2026-04-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_04 PARTITION OF transacoes
    FOR VALUES FROM ('2026-04-01 00:00:00+00') TO ('2026-05-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_05 PARTITION OF transacoes
    FOR VALUES FROM ('2026-05-01 00:00:00+00') TO ('2026-06-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_06 PARTITION OF transacoes
    FOR VALUES FROM ('2026-06-01 00:00:00+00') TO ('2026-07-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_07 PARTITION OF transacoes
    FOR VALUES FROM ('2026-07-01 00:00:00+00') TO ('2026-08-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_08 PARTITION OF transacoes
    FOR VALUES FROM ('2026-08-01 00:00:00+00') TO ('2026-09-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_09 PARTITION OF transacoes
    FOR VALUES FROM ('2026-09-01 00:00:00+00') TO ('2026-10-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_10 PARTITION OF transacoes
    FOR VALUES FROM ('2026-10-01 00:00:00+00') TO ('2026-11-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_11 PARTITION OF transacoes
    FOR VALUES FROM ('2026-11-01 00:00:00+00') TO ('2026-12-01 00:00:00+00');
CREATE TABLE IF NOT EXISTS transacoes_2026_12 PARTITION OF transacoes
    FOR VALUES FROM ('2026-12-01 00:00:00+00') TO ('2027-01-01 00:00:00+00');

-- -----------------------------------------------------------------------------
-- 3. Transactional Outbox Pattern (Garantia de Entrega SQS)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE', -- PENDENTE, PROCESSADO, FALHA
    tentativas INT NOT NULL DEFAULT 0,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processado_em TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_outbox_pendentes ON outbox_events(status, criado_em) WHERE status = 'PENDENTE';

-- -----------------------------------------------------------------------------
-- 4. Base de Conhecimento RAG Híbrido (Vetorial + Lexical BM25)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documentos_conhecimento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    categoria VARCHAR(50) NOT NULL, -- TAXAS, MAQUININHAS, PIX, CHARGEBACK_COMPLIANCE
    conteudo TEXT NOT NULL,
    metadados JSONB NOT NULL DEFAULT '{}',
    tsv_conteudo tsvector GENERATED ALWAYS AS (to_tsvector('portuguese', conteudo)) STORED,
    embedding vector(1536) NOT NULL,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_documentos_tsv ON documentos_conhecimento USING gin(tsv_conteudo);

CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw 
ON documentos_conhecimento 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- -----------------------------------------------------------------------------
-- 5. Disputas & Chargebacks Auditados
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS disputas_chargeback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transacao_id UUID NOT NULL,
    lojista_id VARCHAR(50) NOT NULL REFERENCES lojistas(id),
    motivo VARCHAR(100) NOT NULL,
    valor_disputado NUMERIC(15, 2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'EM_ANALISE', -- EM_ANALISE, DEFENDIDO, GANHO, PERDIDO
    score_probabilidade_ganho NUMERIC(5, 2),
    dossie_defesa TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
