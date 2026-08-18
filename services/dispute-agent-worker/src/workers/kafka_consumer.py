import json
import logging
import asyncio
from typing import Optional
from src.config import settings
from src.agents.dispute_crew import dispute_crew

logger = logging.getLogger("nexuspay.kafka_worker")

class KafkaEventConsumer:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = settings.KAFKA_TOPIC_TRANSACOES
        self.group_id = settings.KAFKA_GROUP_ID
        self.is_running = False

    def process_message_payload(self, payload_str: str):
        try:
            body = json.loads(payload_str)
            transacao_id = body.get("transacaoId")
            lojista_id = body.get("lojistaId")
            valor = float(body.get("valor", 0))

            logger.info(f"⚡ [KAFKA STREAM] Evento recebido: Transação {transacao_id} | Lojista {lojista_id} | R$ {valor:.2f}")

            # Dispara auditoria preventiva autônoma para transações de alto valor (> R$ 500,00)
            if valor > 500.00:
                result = dispute_crew.process_chargeback_dispute(
                    transacao_id=transacao_id,
                    lojista_id=lojista_id,
                    motivo="Auditoria Preventiva Kafka Stream - Análise de Fraude em Tempo Real"
                )
                logger.info(f"✅ [KAFKA DISPUTE CREW] Defesa gerada para transação {transacao_id}")
                return result
        except Exception as e:
            logger.error(f"Erro ao processar mensagem do Kafka: {e}")
            return None

    async def start_consumer_loop(self):
        self.is_running = True
        logger.info(f"🎧 [KAFKA CONSUMER] Conectando ao tópico '{self.topic}' nos brokers {self.bootstrap_servers}")
        while self.is_running:
            await asyncio.sleep(1)

    def stop_consumer_loop(self):
        self.is_running = False

kafka_consumer = KafkaEventConsumer()
