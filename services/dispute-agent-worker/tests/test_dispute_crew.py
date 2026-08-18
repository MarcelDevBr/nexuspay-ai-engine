import pytest
from src.agents.dispute_crew import dispute_crew

def test_dispute_crew_chargeback_defense():
    res = dispute_crew.process_chargeback_dispute(
        transacao_id="TX_998877",
        lojista_id="lojista_123",
        motivo="Fraude amigável"
    )
    assert res["status"] == "DEFENDIDO_AUTOMATICAMENTE"
    assert res["score_probabilidade_ganho"] >= 90.0
    assert "DOSSIÊ DE DEFESA" in res["dossie_defesa"]
    assert res["evidencias"]["chip_emv_lido"] is True
    assert res["compliance"]["presuncao_legitimidade"] is True
