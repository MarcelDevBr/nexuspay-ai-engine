from src.domain.models import (
    DisputeRequest,
    EvidenceData,
    ComplianceVerdict,
    DisputeDefenseResult
)

def test_dispute_request_model():
    req = DisputeRequest(
        transacao_id="tx_123",
        lojista_id="loj_456",
        motivo="Fraude alegada",
        valor=250.0
    )
    assert req.transacao_id == "tx_123"
    assert req.valor == 250.0

def test_evidence_data_defaults():
    evidence = EvidenceData()
    assert evidence.chip_emv_lido is True
    assert evidence.senha_pessoal_validada is True
    assert evidence.autenticacao_3ds == "COMPLETED"

def test_compliance_verdict_defaults():
    verdict = ComplianceVerdict()
    assert "BACEN" in verdict.normativa_aplicavel
    assert verdict.presuncao_legitimidade is True

def test_dispute_defense_result():
    res = DisputeDefenseResult(
        protocolo="PROT-1234",
        transacao_id="tx_123",
        lojista_id="loj_456",
        status="DEFENDIDO_AUTOMATICAMENTE",
        score_probabilidade_ganho=94.5,
        evidencias=EvidenceData(),
        compliance=ComplianceVerdict(),
        dossie_defesa="Texto da defesa"
    )
    assert res.score_probabilidade_ganho == 94.5
    assert res.status == "DEFENDIDO_AUTOMATICAMENTE"
