package com.nexuspay.infrastructure.messaging;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class KafkaTransactionProducer {

    private static final Logger logFallback = LoggerFactory.getLogger(KafkaTransactionProducer.class);

    @Autowired(required = false)
    private KafkaTemplate<String, String> kafkaTemplate;

    @Value("${nexuspay.kafka.topic.transacoes:nexuspay.transacoes.events}")
    private String topicTransacoes;

    public void publishTransactionEvent(String lojistaId, String eventPayload) {
        if (kafkaTemplate != null) {
            try {
                logFallback.info("📢 [KAFKA PRODUCER] Publicando evento de transação no tópico '{}' com key: {}", topicTransacoes, lojistaId);
                kafkaTemplate.send(topicTransacoes, lojistaId, eventPayload);
            } catch (Exception e) {
                logFallback.warn("⚠️ Falha ao publicar no Kafka (operando em modo resiliente): {}", e.getMessage());
            }
        } else {
            logFallback.info("⚡ [KAFKA MOCK] Evento simulado para o lojista {}: {}", lojistaId, eventPayload);
        }
    }
}
