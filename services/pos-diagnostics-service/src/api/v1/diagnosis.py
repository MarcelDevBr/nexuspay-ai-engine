from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from src.services.handlers import diagnostics_engine
from src.domain.models import DiagnosticResult

router = APIRouter(prefix="/api/v1/diagnosis", tags=["POS Diagnostics"])

class PosDiagnosisRequest(BaseModel):
    terminal_id: str = Field(..., description="ID da maquininha POS Stone")
    error_code: Optional[str] = Field(None, description="Código de erro retornado pela maquininha")
    description: str = Field(..., description="Descrição da falha relatada pelo lojista")

@router.post("/pos", response_model=DiagnosticResult)
async def diagnose_pos(request: PosDiagnosisRequest):
    return diagnostics_engine.diagnose(
        terminal_id=request.terminal_id,
        error_code=request.error_code,
        description=request.description
    )
