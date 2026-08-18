import pytest
from src.agents.dispute_crew import (
    EvidenceExtractorAgent,
    ComplianceAuditorAgent,
    LegalDefenseAgent,
    DisputeResolutionCrew
)
from src.domain.models import EvidenceData, ComplianceVerdict

def test_evidence_extractor_agent():
    agent = EvidenceExtractorAgent()
    evidence = agent.extract_evidence("TX_1", "lojista_123")
    assert evidence.chip_emv_lido is True
    assert evidence.senha_pessoal_validada is True
    assert evidence.terminal_id == "POS_STONE_9876"

def test_compliance_auditor_agent_legitimate():
    agent = ComplianceAuditorAgent()
    evidence = EvidenceData(chip_emv_lido=True, senha_pessoal_validada=True)
    verdict = agent.audit_compliance(evidence, "Fraude")
    assert verdict.presuncao_legitimidade is True
    assert verdict.motivo_valido_defesa is True

def test_compliance_auditor_agent_not_legitimate():
    agent = ComplianceAuditorAgent()
    evidence = EvidenceData(chip_emv_lido=False, senha_pessoal_validada=False)
    verdict = agent.audit_compliance(evidence, "Fraude")
    assert verdict.presuncao_legitimidade is False

def test_legal_defense_agent_dossier():
    agent = LegalDefenseAgent()
    evidence = EvidenceData(chip_emv_lido=True, senha_pessoal_validada=True)
    compliance = ComplianceVerdict(presuncao_legitimidade=True)
    dossier = agent.generate_defense_dossier("TX_1", "lojista_123", "Fraude", evidence, compliance)
    assert "DOSSIÊ DE DEFESA" in dossier
    assert "TX_1" in dossier
    assert "lojista_123" in dossier

def test_dispute_resolution_crew_custom_mocks():
    class MockExtractor:
        def extract_evidence(self, t_id, l_id):
            return EvidenceData(chip_emv_lido=False, senha_pessoal_validada=False)

    crew = DisputeResolutionCrew(extractor=MockExtractor())
    result = crew.process_chargeback_dispute("TX_MOCK", "lojista_999", "Não reconhece compra")
    assert result.status == "DEFENDIDO_AUTOMATICAMENTE"
    assert result.score_probabilidade_ganho == 50.00
    assert result.transacao_id == "TX_MOCK"

def test_dispute_resolution_crew_default():
    crew = DisputeResolutionCrew()
    result = crew.process_chargeback_dispute("TX_DEF", "lojista_123", "Fraude Amigável")
    assert result.score_probabilidade_ganho == 94.50
    assert result.evidencias.chip_emv_lido is True
