from abc import ABC, abstractmethod
from src.domain.models import EvidenceData, ComplianceVerdict

class IEvidenceExtractorAgent(ABC):
    @abstractmethod
    def extract_evidence(self, transacao_id: str, lojista_id: str) -> EvidenceData:
        pass

class IComplianceAuditorAgent(ABC):
    @abstractmethod
    def audit_compliance(self, evidence: EvidenceData, motivo: str) -> ComplianceVerdict:
        pass

class ILegalDefenseAgent(ABC):
    @abstractmethod
    def generate_defense_dossier(self, transacao_id: str, lojista_id: str, motivo: str, evidence: EvidenceData, compliance: ComplianceVerdict) -> str:
        pass
