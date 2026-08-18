package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class StatusTransacaoTest {

    @Test
    void testEnumValues() {
        for (StatusTransacao status : StatusTransacao.values()) {
            assertNotNull(status.name());
        }
    }
}
