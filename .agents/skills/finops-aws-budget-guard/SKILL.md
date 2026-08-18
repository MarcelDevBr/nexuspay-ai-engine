---
name: finops-aws-budget-guard
description: >-
  Diretrizes de FinOps, controle de custos e travas do AWS Free Tier. Use para garantir que todas
  as integrações em nuvem e execuções locais mantenham custo zero através de LocalStack, Mock Providers
  e limites estritos de orçamento via AWS Budgets.
---

# FinOps & AWS Budget Guard Skill

## Regras de Execução

1. **Desenvolvimento Local e CI:** Sempre use `LocalStack` e `USE_MOCK_LLM=true`.
2. **AWS Real:** Se conectar a uma conta real da AWS, certifique-se de que o recurso `aws_budgets_budget` no Terraform esteja ativo com o limite mensal de $1.00.
3. **Semantic Cache:** Sempre valide se perguntas repetidas estão batendo no Cache Semântico do Redis antes de invocar modelos na nuvem.
