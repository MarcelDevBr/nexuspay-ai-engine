import pytest
from src.ports.diagnostic_handler import IDiagnosticStrategy
from src.domain.models import DiagnosticResult

class ConcreteDiagnosticStrategy(IDiagnosticStrategy):
    def can_handle(self, error_code, description):
        return True

    def execute(self, terminal_id, error_code, description):
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="OK",
            action_taken="none",
            status="RESOLVED",
            instrucoes_lojista="Tudo certo"
        )

def test_idiagnostic_strategy_implementation():
    strategy = ConcreteDiagnosticStrategy()
    assert strategy.can_handle("ERR_01", "Falha teste") is True
    res = strategy.execute("term_123", "ERR_01", "Falha teste")
    assert res.terminal_id == "term_123"

def test_idiagnostic_strategy_abstract_methods():
    with pytest.raises(TypeError):
        # Não pode instanciar classe abstrata diretamente
        IDiagnosticStrategy()
