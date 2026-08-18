package com.nexuspay.infrastructure.messaging;

import com.nexuspay.domain.model.OutboxEvent;
import com.nexuspay.infrastructure.persistence.OutboxEventRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.data.domain.Pageable;
import org.springframework.test.util.ReflectionTestUtils;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;

import java.util.Collections;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class OutboxPublisherSchedulerTest {

    private OutboxEventRepository outboxEventRepository;
    private SqsClient sqsClient;
    private KafkaTransactionProducer kafkaProducer;
    private OutboxPublisherScheduler scheduler;

    @BeforeEach
    void setUp() {
        outboxEventRepository = Mockito.mock(OutboxEventRepository.class);
        sqsClient = Mockito.mock(SqsClient.class);
        kafkaProducer = Mockito.mock(KafkaTransactionProducer.class);

        scheduler = new OutboxPublisherScheduler(outboxEventRepository, sqsClient);
        ReflectionTestUtils.setField(scheduler, "kafkaTransactionProducer", kafkaProducer);
        ReflectionTestUtils.setField(scheduler, "queueUrl", "http://localhost:4566/000000000000/transacoes-events");
    }

    @Test
    void testPublishPendingEventsEmpty() {
        when(outboxEventRepository.findTopPendingEvents(any(Pageable.class))).thenReturn(Collections.emptyList());
        scheduler.publishPendingEvents();
        verify(sqsClient, never()).sendMessage(any(SendMessageRequest.class));
    }

    @Test
    void testPublishPendingEventsSuccess() {
        OutboxEvent event = new OutboxEvent("Transacao", "loj_123", "EVENT", "{\"valor\": 200}");
        event.setId(UUID.randomUUID());

        when(outboxEventRepository.findTopPendingEvents(any(Pageable.class))).thenReturn(List.of(event));

        scheduler.publishPendingEvents();

        assertEquals("PROCESSADO", event.getStatus());
        verify(kafkaProducer).publishTransactionEvent(eq("loj_123"), eq("{\"valor\": 200}"));
        verify(sqsClient).sendMessage(any(SendMessageRequest.class));
        verify(outboxEventRepository).save(event);
    }

    @Test
    void testPublishPendingEventsFailureIncrementsAttempts() {
        OutboxEvent event = new OutboxEvent("Transacao", "loj_123", "EVENT", "{\"valor\": 200}");
        event.setId(UUID.randomUUID());

        when(outboxEventRepository.findTopPendingEvents(any(Pageable.class))).thenReturn(List.of(event));
        when(sqsClient.sendMessage(any(SendMessageRequest.class))).thenThrow(new RuntimeException("SQS timeout"));

        scheduler.publishPendingEvents();

        assertEquals(1, event.getTentativas());
        verify(outboxEventRepository).save(event);
    }
}
