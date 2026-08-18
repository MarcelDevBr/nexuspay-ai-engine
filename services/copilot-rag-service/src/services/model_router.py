import logging
from typing import Literal

logger = logging.getLogger("nexuspay.model_router")

ModelTier = Literal["LIGHT_MODEL", "HEAVY_REASONING_MODEL"]

class SmartModelRouter:
    COMPLEX_KEYWORDS = [
        "disputa", "chargeback", "fraude", "conciliação", "auditoria", 
        "divergência", "dossiê", "bacen", "processo"
    ]

    def route_request(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()
        is_complex = any(keyword in prompt_lower for keyword in self.COMPLEX_KEYWORDS)
        
        if is_complex or len(prompt.split()) > 35:
            model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
            tier: ModelTier = "HEAVY_REASONING_MODEL"
            estimated_cost = "$0.003 / 1k tokens"
        else:
            model_id = "meta.llama3-8b-instruct-v1:0"
            tier: ModelTier = "LIGHT_MODEL"
            estimated_cost = "$0.0003 / 1k tokens (90% economia)"

        return {
            "tier": tier,
            "selected_model": model_id,
            "estimated_cost": estimated_cost,
            "is_complex": is_complex
        }

model_router = SmartModelRouter()
