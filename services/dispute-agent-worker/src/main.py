import asyncio
import logging
from src.workers.sqs_consumer import sqs_consumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nexuspay.dispute_main")

async def main():
    logger.info("🚀 Iniciando NexusPay Dispute Agent Worker...")
    try:
        await sqs_consumer.start_polling()
    except KeyboardInterrupt:
        logger.info("🛑 Encerrando worker...")
        sqs_consumer.stop_polling()

if __name__ == "__main__":
    asyncio.run(main())
