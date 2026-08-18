from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.copilot import router as copilot_router

app = FastAPI(
    title="NexusPay Copilot RAG Service",
    description="Microservice responsible for Hybrid RAG and Semantic Cache",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "nexuspay-copilot-rag-service",
        "version": "1.0.0"
    }

app.include_router(copilot_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
