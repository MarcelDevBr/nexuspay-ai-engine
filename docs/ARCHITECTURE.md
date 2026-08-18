# 📐 Arquitetura Detalhada do NexusPay AI Engine

Este documento detalha os padrões arquiteturais, princípios de Clean Architecture, estratégias de resiliência e contratos de comunicação do **NexusPay AI Engine**.

---

## 🏛️ 1. Princípios Fundamentais de Engenharia

O NexusPay foi projetado com base em quatro pilares inegociáveis:
1. **SOLID & Clean Architecture:** Cada microsserviço isola regras de domínio de frameworks e adaptadores de infraestrutura.
2. **FinOps & Zero-Cost Cloud:** Infraestrutura planejada para validações locais em **LocalStack** e modelos LLM mockados, com travas de orçamento no AWS Budgets.
3. **Segurança & Conformidade PCI-DSS / BACEN:** Sanitização perimetral de dados de titulares de cartão (PAN, CVV, CPF) antes de logs ou persistência.
4. **Resiliência Transacional:** Garantia de atomicidade através do padrão **Transactional Outbox**.

---

## 🔄 2. Padrões de Projeto Utilizados

### A. Transactional Outbox Pattern (`services/transaction-ledger-service`)
Ao autorizar uma transação financeira, o sistema precisa notificar outros serviços via **Amazon SQS**. Para evitar estados inconsistentes (transação gravada no banco mas mensagem falha ao ser enviada), utilizamos o Transactional Outbox:
1. O `TransacaoService` grava a entidade `Transacao` e o `OutboxEvent` na mesma transação atômica do PostgreSQL.
2. O componente agendador `OutboxPublisherScheduler` faz a leitura dos eventos com status `PENDENTE` e os publica de forma confiável no Amazon SQS.
3. Após a confirmação de recebimento do SQS, o status é alterado para `PROCESSADO`.

### B. Strategy Pattern para Diagnóstico de POS (`services/pos-diagnostics-service`)
O motor de diagnóstico utiliza a interface `IDiagnosticStrategy`:
- `CryptoKeyDiagnosticHandler`: Ativado para falhas criptográficas EMV (ex.: `ERR_58`).
- `EmvChipDiagnosticHandler`: Ativado para erros de leitura física de chip.
- `ConnectivityDiagnosticHandler`: Ativado para perdas de sinal GPRS/Wi-Fi.

Novos diagnósticos podem ser adicionados sem alterar o código existente (**Open/Closed Principle**).

### C. Multi-Agent Orchestration (`services/dispute-agent-worker`)
Utiliza o framework **CrewAI** com tarefas e papéis segregados:
- **Agente 1 (Extrator de Evidências):** Filtra metadados técnicos de telemetria e valida autenticidade de chip EMV.
- **Agente 2 (Auditor de Compliance):** Compara prazos e regulamentos de bandeiras de cartão (Visa, Mastercard, Elo).
- **Agente 3 (Redator Jurídico):** Constrói a contestação fundamentada com base nos relatórios dos agentes anteriores.

---

## 🐘 3. Estratégia de Dados e Indexação Vetorial

### A. Índices HNSW no pgvector
Para o assistente de RAG, os documentos de regras e manuais são indexados usando o algoritmo **HNSW (Hierarchical Navigable Small World)**:
```sql
CREATE INDEX idx_documentos_embedding_hnsw 
ON documentos_conhecimento 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```
O HNSW oferece busca com complexidade $O(\log N)$, proporcionando recuperação vetorial em menos de 5ms mesmo com milhões de vetores.

### B. Particionamento Nativo de Tabelas
A tabela `transacoes` é particionada por data para permitir alta taxa de ingestão e manutenção eficiente:
```sql
CREATE TABLE transacoes (
    id UUID NOT NULL,
    lojista_id VARCHAR(50) NOT NULL,
    valor NUMERIC(15, 2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, criado_em)
) PARTITION BY RANGE (criado_em);
```

---

## 🛡️ 4. Conformidade PCI-DSS & Segurança

1. **Sanitização de PII no Edge Gateway:**
   - Expressões regulares pré-compiladas identificam números de cartões de 13 a 19 dígitos e aplicam algoritmo de mascaramento preservando apenas os 4 últimos dígitos.
   - Qualquer ocorrência de CVV é substituída por `[REDACTED]`.
2. **Isolamento de Contêineres:**
   - Todos os Dockerfiles utilizam usuários não-root (`USER spring:spring` no Java, `USER appuser` no Python e `runAsNonRoot: true` nos manifestos Kubernetes).
3. **Auditoria Contínua:**
   - Pipelines automatizados com **Semgrep** e **Trivy** verificam vulnerabilidades de dependências e más práticas em tempo de build.
