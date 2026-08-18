from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DisputeRequest(BaseModel):
    transacao_id: str
    lojista_id: str
    motivo: str
    valor: Optional[float] = 0.0

class EvidenceData(BaseModel):
    chip_emv_lido: bool = True
    senha_pessoal_validada: bool = True
    terminal_id: str = "POS_STONE_9876"
    autenticacao_3ds: str = "COMPLETED"
    geolocalizacao_compativel: bool = True

class ComplianceVerdict(BaseModel):
    normativa_aplicavel: str = "BACEN Resolução 150 & Visa Dispute Management"
    presuncao_legitimidade: bool = True
    motivo_valido_defesa: bool = True

class DisputeDefenseResult(BaseModel):
    protocolo: str
    transacao_id: str
    lojista_id: str
    status: str
    score_probabilidade_ganho: float
    evidencias: EvidenceData
    compliance: ComplianceVerdict
    dossie_defesa: str
