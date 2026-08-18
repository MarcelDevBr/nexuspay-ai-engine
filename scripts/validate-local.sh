#!/usr/bin/env bash
set -e

echo "================================================================"
echo "🚀 Iniciando Validação Local Completa do NexusPay AI Engine"
echo "================================================================"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Edge Gateway
echo -e "\n${BLUE}▶ 1/5: Testando Edge Gateway (Node.js/Fastify/Jest)...${NC}"
cd "$ROOT_DIR/services/edge-gateway"
yarn test --silent
yarn build
echo -e "${GREEN}✔ Edge Gateway OK!${NC}"

# 2. Transaction Ledger Service
echo -e "\n${BLUE}▶ 2/5: Testando Transaction Ledger Service (Java/Spring Boot)...${NC}"
cd "$ROOT_DIR/services/transaction-ledger-service"
./mvnw test -q
echo -e "${GREEN}✔ Transaction Ledger Service OK!${NC}"

# 3. Copilot RAG Service
echo -e "\n${BLUE}▶ 3/5: Testando Copilot RAG Service (Python/FastAPI)...${NC}"
cd "$ROOT_DIR/services/copilot-rag-service"
uv run --with pytest --with pytest-asyncio --with numpy --with pydantic --with pydantic-settings --with redis --with fastapi --with psycopg2-binary pytest -q
echo -e "${GREEN}✔ Copilot RAG Service OK!${NC}"

# 4. POS Diagnostics Service
echo -e "\n${BLUE}▶ 4/5: Testando POS Diagnostics Service (Python/FastAPI)...${NC}"
cd "$ROOT_DIR/services/pos-diagnostics-service"
uv run --with pytest --with pytest-asyncio --with pydantic --with pydantic-settings --with fastapi --with httpx pytest -q
echo -e "${GREEN}✔ POS Diagnostics Service OK!${NC}"

# 5. Dispute Agent Worker
echo -e "\n${BLUE}▶ 5/5: Testando Dispute Agent Worker (Python/CrewAI)...${NC}"
cd "$ROOT_DIR/services/dispute-agent-worker"
uv run --with pytest --with pydantic --with pydantic-settings --with boto3 pytest -q
echo -e "${GREEN}✔ Dispute Agent Worker OK!${NC}"

echo -e "\n================================================================"
echo -e "${GREEN}🎉 SUCESSO: Todos os 5 microsserviços foram validados localmente!${NC}"
echo -e "${GREEN}Seu código está pronto e 100% seguro para commit e push.${NC}"
echo "================================================================"
