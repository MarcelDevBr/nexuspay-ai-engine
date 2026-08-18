from typing import Optional, List
from src.ports.diagnostic_handler import IDiagnosticStrategy
from src.domain.models import DiagnosticResult, ErrorCode

class CryptoKeyDiagnosticHandler(IDiagnosticStrategy):
    def can_handle(self, error_code: Optional[str], description: str) -> bool:
        desc_lower = description.lower()
        return error_code == ErrorCode.CRYPTO_KEY_ERROR or "criptografia" in desc_lower or "chave" in desc_lower or "pinpad" in desc_lower

    def execute(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="Falha de sincronismo de chave criptográfica Master/Session (EMV Key Failure).",
            action_taken="reset_pos_security_keys(terminal_id)",
            status="RESOLVED",
            instrucoes_lojista="As chaves de segurança foram renovadas com sucesso via canal seguro TLS. O terminal reiniciará automaticamente em 10 segundos."
        )

class EmvChipDiagnosticHandler(IDiagnosticStrategy):
    def can_handle(self, error_code: Optional[str], description: str) -> bool:
        desc_lower = description.lower()
        return error_code == ErrorCode.EMV_CHIP_ERROR or "chip" in desc_lower or "leitura" in desc_lower

    def execute(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="Falha nos contatos do leitor de chip EMV físico.",
            action_taken="calibrate_chip_reader_sensor(terminal_id)",
            status="RESOLVED",
            instrucoes_lojista="Sensor do leitor calibrado remotamente. Limpe os contatos do cartão e tente novamente."
        )

class ConnectivityDiagnosticHandler(IDiagnosticStrategy):
    def can_handle(self, error_code: Optional[str], description: str) -> bool:
        desc_lower = description.lower()
        return error_code == ErrorCode.CONNECTIVITY_TIMEOUT or "sinal" in desc_lower or "4g" in desc_lower or "wifi" in desc_lower or "rede" in desc_lower

    def execute(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="Instabilidade na antena 4G / GPRS do terminal.",
            action_taken="check_telemetry_connectivity(terminal_id)",
            status="RESOLVED",
            instrucoes_lojista="Conexão remota reiniciada. Sugerido alternar temporariamente para rede Wi-Fi caso o sinal persista fraco."
        )

class GenericDiagnosticHandler(IDiagnosticStrategy):
    def can_handle(self, error_code: Optional[str], description: str) -> bool:
        return True

    def execute(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="Análise de telemetria geral concluída.",
            action_taken="perform_general_healthcheck(terminal_id)",
            status="RESOLVED",
            instrucoes_lojista="Terminal operando dentro dos parâmetros nominais. Reinicie a maquininha caso a falha persista."
        )

class PosDiagnosticsEngine:
    """
    Engine que orquestra as estratégias de diagnóstico (Dependency Inversion & Open/Closed)
    """
    def __init__(self, strategies: Optional[List[IDiagnosticStrategy]] = None):
        self.strategies = strategies or [
            CryptoKeyDiagnosticHandler(),
            EmvChipDiagnosticHandler(),
            ConnectivityDiagnosticHandler(),
            GenericDiagnosticHandler()
        ]

    def diagnose(self, terminal_id: str, error_code: Optional[str], description: str) -> DiagnosticResult:
        for strategy in self.strategies:
            if strategy.can_handle(error_code, description):
                return strategy.execute(terminal_id, error_code, description)
        return DiagnosticResult(
            terminal_id=terminal_id,
            diagnostico="Análise de telemetria geral concluída.",
            action_taken="perform_general_healthcheck(terminal_id)",
            status="RESOLVED",
            instrucoes_lojista="Terminal operando dentro dos parâmetros nominais."
        )

diagnostics_engine = PosDiagnosticsEngine()
