---
name: nexuspay-architecture
description: >-
  Guia e padrões de arquitetura do NexusPay AI Engine. Use para entender o funcionamento dos 5
  microsserviços especializados (Edge Gateway, Transaction Ledger, Copilot RAG, POS Diagnostics
  e Dispute Worker), além dos padrões Monorepo, PostgreSQL pgvector e LocalStack.
---

# NexusPay Architecture Skill

## Visão Geral dos Microsserviços

1. **`services/edge-gateway` (Node.js 26 / Fastify 5):** Proxy reverso, Rate Limiting, sanitização PII (PCI-DSS) e streaming SSE.
2. **`services/transaction-ledger-service` (Java 26 / Spring Boot 4):** Autorização transacional, Ledger ACID, lock pessimista e Transactional Outbox.
3. **`services/copilot-rag-service` (Python 3.14 / FastAPI):** RAG Híbrido com pgvector e Semantic Cache vetorial no Redis.
4. **`services/pos-diagnostics-service` (Python 3.14 / FastAPI):** Telemetria de POS e remediação determinística.
5. **`services/dispute-agent-worker` (Python 3.14 / CrewAI):** Multi-agentes autônomos assíncronos via SQS.

## Padrões de Código
- Sempre respeite o Clean Architecture e os princípios SOLID.
- Isole regras de domínio em `domain/`, interfaces em `ports/` e implementações em `services/`.
