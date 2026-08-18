---
name: dispute-agents-orchestration
description: >-
  Orquestração de Multi-Agentes para resolução de contestações de chargebacks financeiros.
  Use para implementar ou testar fluxos dos 3 agentes autônomos (Extrator de Evidências,
  Auditor de Compliance de Bandeiras e Redator Jurídico-Financeiro).
---

# Dispute Agents Orchestration Skill

## Papéis dos Agentes

1. **`EvidenceExtractorAgent`:** Coleta logs EMV, dados de captura com chip/PIN, geolocalização e comprovantes.
2. **`ComplianceAuditorAgent`:** Valida regras das bandeiras (Visa Core Rules / Mastercard) e Resolução BACEN 150.
3. **`LegalDefenseAgent`:** Redige a peça formal de defesa probatória com score de probabilidade de reversão.
