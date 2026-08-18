package com.nexuspay.infrastructure.messaging;

import com.nexuspay.domain.model.OutboxEvent;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
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

    private final OutboxEventRepository outboxEventRepository;
    private final SqsClient sqsClient;

    @Value("${aws.sqs.queue-url:http://localhost:4566/000000000000/transacoes-events}")
    private String queueUrl;

    @Scheduled(fixedDelay = 5000)
    @Transactional
    public void publishPendingEvents() {
        List<OutboxEvent> pendingEvents = outboxEventRepository.findTopPendingEvents(PageRequest.of(0, 50));

        if (pendingEvents.isEmpty()) {
            return;
        }

        log.debug("Processando {} eventos pendentes no Transactional Outbox", pendingEvents.size());

        for (OutboxEvent event : pendingEvents) {
            try {
                SendMessageRequest sendMsgRequest = SendMessageRequest.builder()
                        .queueUrl(queueUrl)
                        .messageBody(event.getPayload())
                        .build();

                sqsClient.sendMessage(sendMsgRequest);

                event.setStatus("PROCESSADO");
                event.setProcessadoEm(OffsetDateTime.now());
                log.info("Evento publicado com sucesso no SQS! EventID: {}, AggregateID: {}", event.getId(), event.getAggregateId());
            } catch (Exception e) {
                log.warn("Tentativa de publicação falhou para o evento {}: {}. Será retentado no próximo ciclo.", event.getId(), e.getMessage());
                event.setTentativas(event.getTentativas() + 1);
                if (event.getTentativas() > 5) {
                    event.setStatus("FALHA");
                }
            }
            outboxEventRepository.save(event);
        }
    }
}
