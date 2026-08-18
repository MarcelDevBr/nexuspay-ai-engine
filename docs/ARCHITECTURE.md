# 📐 Arquitetura Detalhada do NexusPay AI Engine

Este documento detalha os padrões arquiteturais, princípios de Clean Architecture, estratégias de resiliência, topologia de nuvem **AWS (Amazon Web Services)** e contratos de comunicação do **NexusPay AI Engine**.

---

## 🏛️ 1. Princípios Fundamentais de Engenharia

O NexusPay foi projetado com base em quatro pilares inegociáveis:
1. **SOLID & Clean Architecture:** Cada microsserviço isola regras de domínio de frameworks e adaptadores de infraestrutura (Ports & Adapters / Hexagonal Architecture).
2. **FinOps & Zero-Cost Cloud:** Infraestrutura planejada para validações locais em **LocalStack** e modelos LLM mockados, com travas de orçamento no AWS Budgets ($1.00 USD).
3. **Segurança & Conformidade PCI-DSS / BACEN:** Sanitização perimetral de dados de titulares de cartão (PAN, CVV, CPF) antes de logs ou persistência, além de retenção fiscal de 5 anos via Amazon S3 Glacier.
4. **Resiliência Transacional:** Garantia de atomicidade através do padrão **Transactional Outbox** com persistência no PostgreSQL 16 e publicação dual em **Apache Kafka / Amazon MSK** e **Amazon SQS**.

---

## 🛠️ 2. Detalhamento da Stack Tecnológica por Camada

```
+-----------------------------------------------------------------------------------+
| 🌐 1. EDGE LAYER (Node.js 26 LTS + Fastify 5 + TypeScript 5.7)                    |
|    - PII Masking Engine (Regex PCI-DSS em tempo de voo)                           |
|    - SSE (Server-Sent Events) Streaming Manager                                   |
|    - Rate Limiting Distribuído (Redis 7 Backend)                                  |
+-----------------------------------------------------------------------------------+
| ☕ 2. CORE TRANSACTIONAL (Java 26 + Spring Boot 4 + Lombok)                       |
|    - Virtual Threads (Project Loom) Concurrency Model                             |
|    - Generational ZGC (Pausas de Coleta de Lixo < 1ms)                            |
|    - Transactional Outbox Pattern (JPA + Kafka + SQS Publisher)                   |
+-----------------------------------------------------------------------------------+
| 💬 3. COGNITIVE & RAG ENGINE (Python 3.14 + FastAPI + pgvector + Redis)           |
|    - Hybrid RAG (pgvector HNSW Cosine Similarity + BM25 Lexical Search)           |
|    - Redis Semantic Cache (Cosine Distance >= 0.92 -> Resposta em ~10ms / R$ 0,00)|
|    - Dynamic LLM Router (Amazon Bedrock / OpenAI / Local Mock)                    |
+-----------------------------------------------------------------------------------+
| 📟 4. POS DIAGNOSTICS (Python 3.14 + FastAPI + Pydantic v2)                       |
|    - ISO 8583 Protocol Parser & EMV/PINPAD Crypto Key Synchronizer (ERR_58)       |
|    - Strategy Pattern para Diagnósticos Determinísticos (Open/Closed Principle)   |
+-----------------------------------------------------------------------------------+
| 🤖 5. AUTONOMOUS DISPUTE CREW (Python 3.14 + CrewAI + Kafka Consumer + SQS)       |
|    - Multi-Agent Orchestration (Evidence Extractor, Compliance Auditor, Legal)    |
|    - KEDA Event-Driven Horizontal Autoscaling (0 a 10 pods por profundidade SQS)  |
+-----------------------------------------------------------------------------------+
```

---

## ☁️ 3. Topologia e Serviços de Nuvem AWS (Amazon Web Services)

Toda a infraestrutura AWS do projeto é provisionada de forma declarativa via **Terraform** ([`terraform/`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform)) e orquestrada no Kubernetes ([`k8s/`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/k8s)).

### 🗺️ Matriz de Serviços AWS:

| Serviço AWS | Configuração & Recurso IaC | Finalidade no NexusPay |
| :--- | :--- | :--- |
| **Amazon EKS v1.31** | `aws_eks_cluster.nexuspay_eks` ([`eks.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/eks.tf)) | Control Plane gerenciado para orquestração dos 5 microsserviços em namespace isolado (`nexuspay`). |
| **Amazon EC2 Spot** | `aws_eks_node_group.nexuspay_spot_nodes` (`t4g.medium`, `t3.medium`) | Nós computacionais com redução de 90% de custos via instâncias Spot com tolerância a falhas. |
| **AWS ALB Ingress** | AWS Load Balancer Controller L7 ([`k8s/services/01-edge-gateway.yaml`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/k8s/services/01-edge-gateway.yaml)) | Balanceamento perimetral de requisições HTTPS, terminação TLS e roteamento para o Edge Gateway. |
| **Amazon RDS PostgreSQL 16** | `aws_db_instance.nexuspay_postgres` ([`rds.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/rds.tf)) | Banco relacional e vetorial unificado com `pgvector` nativo, instâncias `db.t4g.micro` (Free Tier) e partição por range de datas. |
| **Amazon ElastiCache Redis 7** | `aws_elasticache_cluster.nexuspay_redis` ([`elasticache.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/elasticache.tf)) | Cluster em memória (`cache.t4g.micro`) para Cache Semântico de embeddings e Rate Limiting distribuído. |
| **Amazon MSK Serverless** | `aws_msk_serverless_cluster.nexuspay_kafka` ([`msk.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/msk.tf)) | Cluster Kafka gerenciado sem servidor para streaming particionado por `lojista_id` com auth SASL/IAM. |
| **Amazon SQS + DLQ** | `aws_sqs_queue.transacoes_events` e `_dlq` ([`sqs.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/sqs.tf)) | Barramento de mensageria assíncrona desacoplado com Redrive Policy (5 retentativas) e retenção de 14 dias. |
| **Amazon S3 Vault** | `aws_s3_bucket.nexuspay_storage` ([`s3.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/s3.tf)) | Bucket versionado com criptografia `AES256` para arquivamento de evidências de disputas e manuais RAG. |
| **Amazon S3 Glacier** | `aws_s3_bucket_lifecycle_configuration` ([`s3.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/s3.tf)) | Transição para Glacier após 90 dias e expiração fiscal após 5 anos (1825 dias - Conformidade BACEN). |
| **AWS Budgets** | `aws_budgets_budget.finops_zero_cost_guard` ([`budgets.tf`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/terraform/budgets.tf)) | FinOps Guardrail limitando gasto máximo a **$1.00 USD/mês** com alertas automáticos em 80% e 100%. |
| **AWS IAM / IRSA** | `aws_iam_role.eks_cluster_role` e `eks_node_role` | Concessão de privilégios mínimos para Service Accounts e instâncias sem uso de credenciais estáticas. |
| **Amazon Bedrock** | API de Foundation Models (Claude 3.5 / Titan) | Inferência de IA Generativa e geração de embeddings vetoriais com fallback zero-cost (`USE_MOCK_LLM`). |
| **LocalStack** | Container Docker `localstack/localstack` ([`docker-compose.yml`](file:///home/marcel/Desenvolvimento/Projetos/nexuspay-ai-engine/docker/docker-compose.yml)) | Emulador local dos serviços SQS, S3 e Secrets Manager para testes 100% offline e sem custos. |

---

## 🔄 4. Padrões de Projeto e Event Streaming
 
### A. Apache Kafka / Amazon MSK Event Streaming (`services/transaction-ledger-service` & `dispute-agent-worker`)
Para garantir alta taxa de transferência (dezenas de milhares de eventos por segundo) e desacoplamento com garantia de ordenação por chave (`lojista_id`):
1. O `KafkaTransactionProducer` publica eventos no tópico `nexuspay.transacoes.events`.
2. As partições do Kafka distribuem a carga de acordo com o hash da chave do lojista, garantindo que eventos do mesmo lojista sejam processados na ordem exata de emissão.
3. O `KafkaEventConsumer` do worker de disputas consome o stream com Consumer Group balanceado (`nexuspay-dispute-worker-group`). Transações com suspeita de fraude ou valor elevado disparam automaticamente a esteira autônoma de defesa da CrewAI.
4. No Kubernetes, o **KEDA Kafka ScaledObject** monitora o lag de mensagens nas partições do tópico e escala os pods horizontalmente de forma reativa.

### B. Transactional Outbox Pattern (`services/transaction-ledger-service`)
Ao autorizar uma transação financeira, o sistema precisa notificar outros serviços via **Apache Kafka** e **Amazon SQS**. Para evitar estados inconsistentes (transação gravada no banco mas mensagem falha ao ser enviada), utilizamos o Transactional Outbox:
1. O `TransacaoService` grava a entidade `Transacao` e o `OutboxEvent` na mesma transação atômica do PostgreSQL.
2. O componente agendador `OutboxPublisherScheduler` faz a leitura dos eventos com status `PENDENTE` e os publica de forma confiável no Apache Kafka e Amazon SQS.
3. Após a confirmação de recebimento, o status é alterado para `PROCESSADO`.

### C. Strategy Pattern para Diagnóstico de POS (`services/pos-diagnostics-service`)
O motor de diagnóstico utiliza a interface `IDiagnosticStrategy`:
- `CryptoKeyDiagnosticHandler`: Ativado para falhas criptográficas EMV (ex.: `ERR_58`).
- `EmvChipDiagnosticHandler`: Ativado para erros de leitura física de chip.
- `ConnectivityDiagnosticHandler`: Ativado para perdas de sinal GPRS/Wi-Fi.

Novos diagnósticos podem ser adicionados sem alterar o código existente (**Open/Closed Principle**).

### D. Multi-Agent Orchestration (`services/dispute-agent-worker`)
Utiliza o framework **CrewAI** com tarefas e papéis segregados:
- **Agente 1 (Extrator de Evidências):** Filtra metadados técnicos de telemetria e valida autenticidade de chip EMV.
- **Agente 2 (Auditor de Compliance):** Compara prazos e regulamentos de bandeiras de cartão (Visa, Mastercard, Elo).
- **Agente 3 (Redator Jurídico):** Constrói a contestação fundamentada com base nos relatórios dos agentes anteriores.

---

## 🐘 5. Estratégia de Dados e Indexação Vetorial

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

## 🛡️ 6. Conformidade PCI-DSS & Segurança Perimetral

1. **Sanitização de PII no Edge Gateway:**
   - Expressões regulares pré-compiladas identificam números de cartões de 13 a 19 dígitos e aplicam algoritmo de mascaramento preservando apenas os 4 últimos dígitos (`[CARD_FINAL_4444]`).
   - Qualquer ocorrência de CVV é substituída por `[REDACTED]` e CPF mascarado (`[CPF_PROTEGIDO]`).
2. **Isolamento de Contêineres:**
   - Todos os Dockerfiles utilizam usuários não-root (`USER spring:spring` no Java, `USER appuser` no Python e `runAsNonRoot: true` nos manifestos Kubernetes).
3. **Auditoria Contínua & SAST:**
   - Pipelines automatizados com **Semgrep** (OWASP Top 10 / PCI-DSS) e **Trivy** (vulnerabilidades de dependências) executados a cada commit no GitHub Actions.

