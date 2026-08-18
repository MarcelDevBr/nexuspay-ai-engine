package com.nexuspay.domain.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class TipoTransacaoTest {

    @Test
    void testEnumValues() {
        for (TipoTransacao tipo : TipoTransacao.values()) {
            assertNotNull(tipo.name());
        }
    }
}
