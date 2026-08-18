import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.copilot import router as copilot_router
from src.api.v1.diagnosis import router as diagnosis_router
from src.workers.sqs_consumer import sqs_consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nexuspay.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização: Inicia worker assíncrono do SQS em background task
    logger.info("🚀 Inicializando NexusPay GenAI Engine & Multi-Agent Ecosystem...")
    polling_task = asyncio.create_task(sqs_consumer.start_polling())
    yield
    # Encerramento gracioso
    logger.info("🛑 Encerrando GenAI Engine e desconectando workers...")
    sqs_consumer.stop_polling()
    polling_task.cancel()

app = FastAPI(
    title="NexusPay AI Engine",
    description="Enterprise Polyglot GenAI Platform & Autonomous Multi-Agent Ecosystem",
    version="1.0.0",
    lifespan=lifespan
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
        "service": "nexuspay-ai-core",
        "version": "1.0.0"
    }

app.include_router(copilot_router)
app.include_router(diagnosis_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
