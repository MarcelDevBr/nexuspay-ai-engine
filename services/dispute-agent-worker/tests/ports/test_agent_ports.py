import pytest
from src.ports.agent_ports import (
    IEvidenceExtractorAgent,
    IComplianceAuditorAgent,
    ILegalDefenseAgent
)
from src.domain.models import EvidenceData, ComplianceVerdict

class ConcreteExtractor(IEvidenceExtractorAgent):
    def extract_evidence(self, transacao_id: str, lojista_id: str) -> EvidenceData:
        return EvidenceData()

class ConcreteAuditor(IComplianceAuditorAgent):
    def audit_compliance(self, evidence: EvidenceData, motivo: str) -> ComplianceVerdict:
        return ComplianceVerdict()

class ConcreteLegal(ILegalDefenseAgent):
    def generate_defense_dossier(self, transacao_id, lojista_id, motivo, evidence, compliance) -> str:
        return "Dossiê OK"

def test_agent_ports_implementations():
    extractor = ConcreteExtractor()
    auditor = ConcreteAuditor()
    legal = ConcreteLegal()

    ev = extractor.extract_evidence("tx_1", "loj_1")
    comp = auditor.audit_compliance(ev, "motivo")
    dossie = legal.generate_defense_dossier("tx_1", "loj_1", "motivo", ev, comp)

    assert ev.chip_emv_lido is True
    assert comp.presuncao_legitimidade is True
    assert dossie == "Dossiê OK"

def test_agent_ports_abstract_instantiation():
    with pytest.raises(TypeError):
        IEvidenceExtractorAgent()
    with pytest.raises(TypeError):
        IComplianceAuditorAgent()
    with pytest.raises(TypeError):
        ILegalDefenseAgent()
