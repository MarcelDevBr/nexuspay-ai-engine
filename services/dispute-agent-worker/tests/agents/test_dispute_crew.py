from src.agents.dispute_crew import (
    EvidenceExtractorAgent,
    ComplianceAuditorAgent,
    LegalDefenseAgent,
    DisputeResolutionCrew,
    dispute_crew
)
from src.domain.models import EvidenceData, ComplianceVerdict

def test_evidence_extractor_agent():
    extractor = EvidenceExtractorAgent()
    ev = extractor.extract_evidence("tx_001", "loj_001")
    assert ev.chip_emv_lido is True
    assert ev.senha_pessoal_validada is True
    assert ev.terminal_id == "POS_STONE_9876"

def test_compliance_auditor_agent():
    auditor = ComplianceAuditorAgent()
    ev_valid = EvidenceData(chip_emv_lido=True, senha_pessoal_validada=True)
    verdict = auditor.audit_compliance(ev_valid, "Contestação de fraude")
    assert verdict.presuncao_legitimidade is True

    ev_invalid = EvidenceData(chip_emv_lido=False, senha_pessoal_validada=False)
    verdict_invalid = auditor.audit_compliance(ev_invalid, "Fraude")
    assert verdict_invalid.presuncao_legitimidade is False

def test_legal_defense_agent():
    writer = LegalDefenseAgent()
    ev = EvidenceData()
    comp = ComplianceVerdict()
    dossie = writer.generate_defense_dossier("tx_100", "loj_200", "Chargeback indevido", ev, comp)
    assert "DOSSIÊ DE DEFESA" in dossie
    assert "tx_100" in dossie
    assert "loj_200" in dossie

def test_dispute_resolution_crew_end_to_end():
    crew = DisputeResolutionCrew()
    res = crew.process_chargeback_dispute("tx_777", "loj_777", "Fraude amigável")
    assert res.transacao_id == "tx_777"
    assert res.status == "DEFENDIDO_AUTOMATICAMENTE"
    assert res.score_probabilidade_ganho == 94.50
    assert "DOSSIÊ DE DEFESA" in res.dossie_defesa

def test_dispute_resolution_crew_low_score():
    class MockAuditor(ComplianceAuditorAgent):
        def audit_compliance(self, evidence, motivo):
            return ComplianceVerdict(presuncao_legitimidade=False)

    crew = DisputeResolutionCrew(auditor=MockAuditor())
    res = crew.process_chargeback_dispute("tx_888", "loj_888", "Fraude")
    assert res.score_probabilidade_ganho == 50.00

def test_singleton_dispute_crew():
    assert dispute_crew is not None
    assert isinstance(dispute_crew, DisputeResolutionCrew)
