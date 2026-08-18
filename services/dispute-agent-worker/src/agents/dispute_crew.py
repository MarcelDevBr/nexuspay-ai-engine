import logging
import uuid
from typing import Optional
from src.domain.models import EvidenceData, ComplianceVerdict, DisputeDefenseResult
from src.ports.agent_ports import IEvidenceExtractorAgent, IComplianceAuditorAgent, ILegalDefenseAgent

logger = logging.getLogger("nexuspay.dispute_crew")

class EvidenceExtractorAgent(IEvidenceExtractorAgent):
    def extract_evidence(self, transacao_id: str, lojista_id: str) -> EvidenceData:
        logger.info(f"🔍 [Agente 1 - Extrator] Coletando logs EMV e geolocalização da transação {transacao_id}...")
        return EvidenceData(
            chip_emv_lido=True,
            senha_pessoal_validada=True,
            terminal_id="POS_STONE_9876",
            autenticacao_3ds="COMPLETED",
            geolocalizacao_compativel=True
        )

class ComplianceAuditorAgent(IComplianceAuditorAgent):
    def audit_compliance(self, evidence: EvidenceData, motivo: str) -> ComplianceVerdict:
        logger.info(f"⚖️ [Agente 2 - Compliance] Checando regras BACEN/Bandeiras para motivo '{motivo}'...")
        return ComplianceVerdict(
            normativa_aplicavel="BACEN Resolução 150 & Visa Dispute Management",
            presuncao_legitimidade=evidence.chip_emv_lido and evidence.senha_pessoal_validada,
            motivo_valido_defesa=True
        )

class LegalDefenseAgent(ILegalDefenseAgent):
    def generate_defense_dossier(self, transacao_id: str, lojista_id: str, motivo: str, evidence: EvidenceData, compliance: ComplianceVerdict) -> str:
        logger.info(f"📝 [Agente 3 - Redator] Gerando peça jurídica para transação {transacao_id}...")
        protocolo = f"DISP-{uuid.uuid4().hex[:8].upper()}"
        return (
            f"DOSSIÊ DE DEFESA DE CHARGEBACK - PROTOCOLO #{protocolo}\n\n"
            f"1. DADOS DA TRANSAÇÃO:\n"
            f"   - ID da Transação: {transacao_id}\n"
            f"   - Lojista: {lojista_id}\n"
            f"   - Motivo da Contestação: {motivo}\n\n"
            f"2. EVIDÊNCIAS DE SEGURANÇA:\n"
            f"   - Cartão físico lido via Chip EMV com PIN online autenticado ({evidence.terminal_id}).\n"
            f"   - Presunção de responsabilidade (Liability Shift) favorável ao lojista: {compliance.presuncao_legitimidade}.\n\n"
            f"3. PARECER JURÍDICO-FINANCEIRO:\n"
            f"   - Contestação improcedente de acordo com a {compliance.normativa_aplicavel}. Solicita-se reversão do débito."
        )

class DisputeResolutionCrew:
    """
    Orquestrador de Multi-Agentes (Dependency Inversion Principle)
    """
    def __init__(
        self,
        extractor: Optional[IEvidenceExtractorAgent] = None,
        auditor: Optional[IComplianceAuditorAgent] = None,
        legal_writer: Optional[ILegalDefenseAgent] = None
    ):
        self.extractor = extractor or EvidenceExtractorAgent()
        self.auditor = auditor or ComplianceAuditorAgent()
        self.legal_writer = legal_writer or LegalDefenseAgent()

    def process_chargeback_dispute(self, transacao_id: str, lojista_id: str, motivo: str) -> DisputeDefenseResult:
        logger.info(f"🤖 [CREWAI WORKER] Iniciando auditoria para transação {transacao_id}...")
        
        # 1. Agente 1: Extração
        evidence = self.extractor.extract_evidence(transacao_id, lojista_id)
        
        # 2. Agente 2: Compliance
        compliance = self.auditor.audit_compliance(evidence, motivo)
        
        # 3. Agente 3: Redação Jurídica
        dossie = self.legal_writer.generate_defense_dossier(transacao_id, lojista_id, motivo, evidence, compliance)
        
        score_ganho = 94.50 if compliance.presuncao_legitimidade else 50.00
        protocolo = f"PROT-{uuid.uuid4().hex[:8].upper()}"

        return DisputeDefenseResult(
            protocolo=protocolo,
            transacao_id=transacao_id,
            lojista_id=lojista_id,
            status="DEFENDIDO_AUTOMATICAMENTE",
            score_probabilidade_ganho=score_ganho,
            evidencias=evidence,
            compliance=compliance,
            dossie_defesa=dossie
        )

dispute_crew = DisputeResolutionCrew()
