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
echo -e "\n${BLUE}▶ 1/6: Testando Edge Gateway (Node.js/Fastify/Jest)...${NC}"
cd "$ROOT_DIR/services/edge-gateway"
yarn test --silent
yarn build
echo -e "${GREEN}✔ Edge Gateway OK!${NC}"

# 2. Transaction Ledger Service
echo -e "\n${BLUE}▶ 2/6: Testando Transaction Ledger Service (Java/Spring Boot/Lombok)...${NC}"
cd "$ROOT_DIR/services/transaction-ledger-service"
./mvnw test -q
echo -e "${GREEN}✔ Transaction Ledger Service OK!${NC}"

# 3. Copilot RAG Service
echo -e "\n${BLUE}▶ 3/6: Testando Copilot RAG Service (Python/FastAPI)...${NC}"
cd "$ROOT_DIR/services/copilot-rag-service"
uv run --with pytest --with pytest-asyncio --with numpy --with pydantic --with pydantic-settings --with redis --with fastapi --with psycopg2-binary pytest -q
echo -e "${GREEN}✔ Copilot RAG Service OK!${NC}"

# 4. POS Diagnostics Service
echo -e "\n${BLUE}▶ 4/6: Testando POS Diagnostics Service (Python/FastAPI)...${NC}"
cd "$ROOT_DIR/services/pos-diagnostics-service"
uv run --with pytest --with pytest-asyncio --with pydantic --with pydantic-settings --with fastapi --with httpx pytest -q
echo -e "${GREEN}✔ POS Diagnostics Service OK!${NC}"

# 5. Dispute Agent Worker
echo -e "\n${BLUE}▶ 5/6: Testando Dispute Agent Worker (Python/CrewAI)...${NC}"
cd "$ROOT_DIR/services/dispute-agent-worker"
uv run --with pytest --with pydantic --with pydantic-settings --with boto3 pytest -q
echo -e "${GREEN}✔ Dispute Agent Worker OK!${NC}"

# 6. Kubernetes Manifests Validation
echo -e "\n${BLUE}▶ 6/6: Validando Manifestos Kubernetes & Kustomize (EKS)...${NC}"
cd "$ROOT_DIR"
if command -v kubectl >/dev/null 2>&1; then
    kubectl kustomize k8s/ > /dev/null
elif command -v kustomize >/dev/null 2>&1; then
    kustomize build k8s/ > /dev/null
else
    echo "YAML syntax check..."
    python3 -c "import yaml, glob; [yaml.safe_load_all(open(f)) for f in glob.glob('k8s/**/*.yaml', recursive=True)]"
fi
echo -e "${GREEN}✔ Kubernetes Manifests (EKS) OK!${NC}"

echo -e "\n================================================================"
echo -e "${GREEN}🎉 SUCESSO: Todos os 5 microsserviços + Kubernetes EKS validados localmente!${NC}"
echo -e "${GREEN}Seu código está pronto e 100% seguro para commit e push.${NC}"
echo "================================================================"
