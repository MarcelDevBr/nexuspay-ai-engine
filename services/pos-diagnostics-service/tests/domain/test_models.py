from src.domain.models import ErrorCode, DiagnosticResult

def test_error_code_enum_values():
    assert ErrorCode.CRYPTO_KEY_ERROR == "ERR_58"
    assert ErrorCode.EMV_CHIP_ERROR == "ERR_45"
    assert ErrorCode.CONNECTIVITY_TIMEOUT == "ERR_91"
    assert ErrorCode.GENERIC_HARDWARE == "ERR_99"

def test_diagnostic_result_model():
    result = DiagnosticResult(
        terminal_id="POS_STONE_001",
        diagnostico="Teste diagnóstico",
        action_taken="reboot_terminal()",
        status="RESOLVED",
        instrucoes_lojista="Reiniciando"
    )
    assert result.terminal_id == "POS_STONE_001"
    assert result.status == "RESOLVED"
    assert result.action_taken == "reboot_terminal()"
