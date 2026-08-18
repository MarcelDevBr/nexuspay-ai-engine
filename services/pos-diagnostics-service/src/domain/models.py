from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class ErrorCode(str, Enum):
    CRYPTO_KEY_ERROR = "ERR_58"
    EMV_CHIP_ERROR = "ERR_45"
    CONNECTIVITY_TIMEOUT = "ERR_91"
    GENERIC_HARDWARE = "ERR_99"

class DiagnosticResult(BaseModel):
    terminal_id: str
    diagnostico: str
    action_taken: str
    status: str
    instrucoes_lojista: str
