package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class TransacaoIdTest {

    @Test
    void testEqualsAndHashCode() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();

        TransacaoId id1 = new TransacaoId(id, now);
        TransacaoId id2 = new TransacaoId(id, now);
        TransacaoId id3 = new TransacaoId(UUID.randomUUID(), now);

        assertEquals(id1, id2);
        assertEquals(id1.hashCode(), id2.hashCode());
        assertNotEquals(id1, id3);
        assertNotEquals(id1, null);
        assertNotEquals(id1, "string");
        assertEquals(id1, id1);
    }

    @Test
    void testGettersAndSetters() {
        UUID id = UUID.randomUUID();
        OffsetDateTime now = OffsetDateTime.now();

        TransacaoId transacaoId = new TransacaoId();
        transacaoId.setId(id);
        transacaoId.setCriadoEm(now);

        assertEquals(id, transacaoId.getId());
        assertEquals(now, transacaoId.getCriadoEm());
    }
}
