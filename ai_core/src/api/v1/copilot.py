from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from src.services.rag_service import rag_service
from src.services.model_router import model_router

router = APIRouter(prefix="/api/v1", tags=["Copilot"])

class ChatRequest(BaseModel):
    lojista_id: str = Field(..., description="Identificador do lojista")
    prompt: str = Field(..., description="Pergunta ou solicitação financeira")

class RouteResponse(BaseModel):
    tier: str
    selected_model: str
    estimated_cost: str
    is_complex: bool

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Endpoint SSE: Streaming de tokens com RAG Híbrido e Cache Semântico
    """
    return StreamingResponse(
        rag_service.stream_copilot_response(request.lojista_id, request.prompt),
        media_type="text/event-stream"
    )

@router.post("/chat/route", response_model=RouteResponse)
async def route_chat_prompt(request: ChatRequest):
    """
    Endpoint de Smart Routing & FinOps para inspeção de modelo e custo
    """
    return model_router.route_request(request.prompt)
