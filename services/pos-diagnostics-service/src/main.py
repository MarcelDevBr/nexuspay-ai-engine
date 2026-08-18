from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.diagnosis import router as diagnosis_router

app = FastAPI(
    title="NexusPay POS Diagnostics Service",
    description="Microservice responsible for POS telemetry and automated troubleshooting",
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
        "service": "nexuspay-pos-diagnostics-service",
        "version": "1.0.0"
    }

app.include_router(diagnosis_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
