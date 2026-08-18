from src.services.model_router import SmartModelRouter, model_router

def test_model_router_simple_prompt():
    router = SmartModelRouter()
    result = router.route_request("Qual meu saldo atual?")
    assert result["tier"] == "LIGHT_MODEL"
    assert result["is_complex"] is False
    assert "llama3" in result["selected_model"]
    assert "90% economia" in result["estimated_cost"]

def test_model_router_complex_keywords():
    router = SmartModelRouter()
    keywords = ["disputa", "chargeback", "fraude", "conciliação", "auditoria", "divergência", "dossiê", "bacen", "processo"]
    for kw in keywords:
        res = router.route_request(f"Preciso de ajuda com {kw} financeira")
        assert res["tier"] == "HEAVY_REASONING_MODEL"
        assert res["is_complex"] is True
        assert "claude-3-5-sonnet" in res["selected_model"]

def test_model_router_long_prompt():
    router = SmartModelRouter()
    long_prompt = " ".join(["palavra"] * 40)
    res = router.route_request(long_prompt)
    assert res["tier"] == "HEAVY_REASONING_MODEL"

def test_singleton_model_router():
    assert model_router is not None
    assert isinstance(model_router, SmartModelRouter)
