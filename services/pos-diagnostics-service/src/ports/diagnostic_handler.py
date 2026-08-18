from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models import DiagnosticResult

class IDiagnosticStrategy(ABC):
    """
    Interface para estratégias de diagnóstico e remediação (Strategy Pattern & Open/Closed Principle)
    """
    @abstractmethod
    def can_handle(self, error_code: Optional[str], description: str) -> bool:
        """Verifica se esta estratégia é responsável pelo tipo de falha"""
        pass

    @abstractmethod
    def execute(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        """Executa a remediação determinística e retorna o resultado"""
        pass
