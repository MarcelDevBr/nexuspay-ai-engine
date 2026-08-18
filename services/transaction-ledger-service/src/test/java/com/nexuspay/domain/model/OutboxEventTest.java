package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class OutboxEventTest {

    @Test
    void testOutboxEventGettersAndSetters() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();
        OutboxEvent event = new OutboxEvent("Transacao", "tx_1", "TRANSACTION_AUTHORIZED", "{}");

        event.setId(id);
        event.setStatus("PROCESSADO");
        event.setTentativas(1);
        event.setCriadoEm(now);
        event.setProcessadoEm(now);

        assertEquals(id, event.getId());
        assertEquals("Transacao", event.getAggregateType());
        assertEquals("tx_1", event.getAggregateId());
        assertEquals("TRANSACTION_AUTHORIZED", event.getEventType());
        assertEquals("{}", event.getPayload());
        assertEquals("PROCESSADO", event.getStatus());
        assertEquals(1, event.getTentativas());
        assertEquals(now, event.getCriadoEm());
        assertEquals(now, event.getProcessadoEm());
    }

    @Test
    void testOutboxEventConstructor() {
        OutboxEvent event = new OutboxEvent("Transacao", "tx_2", "CREATED", "{\"valor\": 100}");
        assertNotNull(event);
        assertEquals("tx_2", event.getAggregateId());
        assertEquals("PENDENTE", event.getStatus());
    }
}
