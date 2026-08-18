package com.nexuspay.infrastructure.messaging;

import com.nexuspay.domain.model.OutboxEvent;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.PageRequest;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

import java.time.OffsetDateTime;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class OutboxPublisherScheduler {

    private static final Logger logFallback = LoggerFactory.getLogger(OutboxPublisherScheduler.class);

    private final OutboxEventRepository outboxEventRepository;
    private final SqsClient sqsClient;
    
    @Autowired(required = false)
    private KafkaTransactionProducer kafkaTransactionProducer;

    @Value("${aws.sqs.queue-url:http://localhost:4566/000000000000/transacoes-events}")
    private String queueUrl;

    public OutboxPublisherScheduler(OutboxEventRepository outboxEventRepository, SqsClient sqsClient) {
        this.outboxEventRepository = outboxEventRepository;
        this.sqsClient = sqsClient;
    }

    @Scheduled(fixedDelay = 5000)
    @Transactional
    public void publishPendingEvents() {
        List<OutboxEvent> pendingEvents = outboxEventRepository.findTopPendingEvents(PageRequest.of(0, 50));

        if (pendingEvents.isEmpty()) {
            return;
        }

        logFallback.debug("Processando {} eventos pendentes no Transactional Outbox", pendingEvents.size());

        for (OutboxEvent event : pendingEvents) {
            try {
                // 1. Streaming em Tempo Real para o Apache Kafka
                if (kafkaTransactionProducer != null) {
                    kafkaTransactionProducer.publishTransactionEvent(event.getAggregateId(), event.getPayload());
                }

                // 2. Notificação Assíncrona no Amazon SQS
                SendMessageRequest sendMsgRequest = SendMessageRequest.builder()
                        .queueUrl(queueUrl)
                        .messageBody(event.getPayload())
                        .build();

                sqsClient.sendMessage(sendMsgRequest);

                event.setStatus("PROCESSADO");
                event.setProcessadoEm(OffsetDateTime.now());
                logFallback.info("Evento publicado no Kafka & SQS com sucesso! EventID: {}", event.getId());
            } catch (Exception e) {
                logFallback.warn("Tentativa de publicação falhou para o evento {}: {}", event.getId(), e.getMessage());
                event.setTentativas(event.getTentativas() + 1);
                if (event.getTentativas() > 5) {
                    event.setStatus("FALHA");
                }
            }
            outboxEventRepository.save(event);
        }
    }
}
