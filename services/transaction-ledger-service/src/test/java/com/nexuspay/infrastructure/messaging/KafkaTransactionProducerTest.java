package com.nexuspay.infrastructure.messaging;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;

class KafkaTransactionProducerTest {

    private KafkaTemplate<String, String> kafkaTemplate;
    private KafkaTransactionProducer producer;

    @BeforeEach
    void setUp() {
        kafkaTemplate = Mockito.mock(KafkaTemplate.class);
        producer = new KafkaTransactionProducer();
        ReflectionTestUtils.setField(producer, "kafkaTemplate", kafkaTemplate);
        ReflectionTestUtils.setField(producer, "topicTransacoes", "nexuspay.transacoes.events");
    }

    @Test
    void testPublishTransactionEventWithKafkaTemplate() {
        producer.publishTransactionEvent("loj_123", "{\"valor\": 100}");
        verify(kafkaTemplate).send(eq("nexuspay.transacoes.events"), eq("loj_123"), eq("{\"valor\": 100}"));
    }

    @Test
    void testPublishTransactionEventMockFallback() {
        KafkaTransactionProducer mockProducer = new KafkaTransactionProducer();
        ReflectionTestUtils.setField(mockProducer, "kafkaTemplate", null);
        mockProducer.publishTransactionEvent("loj_123", "{\"valor\": 100}");
    }
}
