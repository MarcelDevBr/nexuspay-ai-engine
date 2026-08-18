import json
import logging
import asyncio
import boto3
from src.config import settings
from src.agents.dispute_crew import dispute_crew

logger = logging.getLogger("nexuspay.sqs_worker")

class SqsEventConsumer:
    def __init__(self):
        self.queue_url = settings.SQS_QUEUE_URL
        self.is_running = False

    def get_sqs_client(self):
        return boto3.client(
            "sqs",
            region_name=settings.AWS_REGION,
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    async def start_polling(self):
        self.is_running = True
        logger.info(f"📬 [SQS WORKER] Iniciando polling assíncrono da fila: {self.queue_url}")
        
        while self.is_running:
            try:
                sqs = self.get_sqs_client()
                response = sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=2
                )
                
                messages = response.get("Messages", [])
                for msg in messages:
                    body = json.loads(msg["Body"])
                    logger.info(f"📨 [SQS EVENT CONSUMED] Processando transação recebida do Java: {body.get('transacaoId')}")
                    
                    # Se a transação for de valor alto ou suspeita, dispara auditoria automática
                    if float(body.get("valor", 0)) > 1000.00:
                        dispute_crew.process_chargeback_dispute(
                            transacao_id=body.get("transacaoId"),
                            lojista_id=body.get("lojistaId"),
                            motivo="Auditoria Preventiva de Risco"
                        )

                    # Deleta mensagem da fila após sucesso
                    sqs.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=msg["ReceiptHandle"]
                    )
            except Exception as e:
                logger.debug(f"Aguardando mensagens na fila SQS ({e})...")
                await asyncio.sleep(5)

    def stop_polling(self):
        self.is_running = False

sqs_consumer = SqsEventConsumer()
